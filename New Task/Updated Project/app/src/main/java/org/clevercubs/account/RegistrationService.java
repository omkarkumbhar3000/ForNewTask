package org.clevercubs.account;

import java.time.Instant;
import java.time.LocalDate;
import java.util.Locale;
import java.util.Map;

import jakarta.validation.Valid;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

import org.clevercubs.audit.AuditLog;
import org.clevercubs.child.ChildService;
import org.clevercubs.child.ChildService.ChildInput;
import org.clevercubs.platform.security.AccountPrincipal;
import org.clevercubs.platform.security.PasswordPolicy;
import org.clevercubs.platform.security.Role;
import org.clevercubs.platform.settings.Settings;
import org.clevercubs.platform.web.ApiException;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Parent registration with the first child and the parent's consent (requirement sections 6 and 7, DD-09,
 * D67). One transaction: the account, the parent profile, three consent records, the child and the child's
 * Year-1 enrolment are all created, or none is.
 *
 * <p>Fields (DD-09). Mandatory: parent name, email, password, the three consents; the child's first name and
 * date of birth. Optional: parent mobile and city; the child's display name, username (suggested when
 * empty) and avatar. Not collected: address, school, gender, photos.
 */
@Service
public class RegistrationService {

    public record ParentPart(
            @NotBlank(message = "required") @Size(max = 100, message = "is too long") String fullName,
            @NotBlank(message = "required") @Email(message = "must be an email address")
            @Size(max = 254, message = "is too long") String email,
            @NotBlank(message = "required") @Size(max = 200, message = "is too long") String password,
            @Size(max = 20, message = "is too long")
            @Pattern(regexp = "^$|^[+0-9 ()-]{6,20}$", message = "must be a phone number") String mobile,
            @Size(max = 80, message = "is too long") String city) {
    }

    public record ChildPart(
            @NotBlank(message = "required") @Size(max = 40, message = "is too long") String firstName,
            @Size(max = 40, message = "is too long") String displayName,
            @NotNull(message = "required") LocalDate dateOfBirth,
            @Size(max = 20, message = "is too long") String username,
            @Size(max = 30, message = "is too long") String avatarCode) {
    }

    public record RegistrationRequest(
            @Valid @NotNull(message = "required") ParentPart parent,
            @Valid @NotNull(message = "required") ChildPart child,
            Boolean acceptTerms, Boolean acceptPrivacy, Boolean consentChildData) {
    }

    private final JdbcClient jdbc;
    private final PasswordEncoder passwords;
    private final PasswordPolicy policy;
    private final ChildService children;
    private final Settings settings;
    private final AuditLog audit;

    public RegistrationService(JdbcClient jdbc, PasswordEncoder passwords, PasswordPolicy policy,
            ChildService children, Settings settings, AuditLog audit) {
        this.jdbc = jdbc;
        this.passwords = passwords;
        this.policy = policy;
        this.children = children;
        this.settings = settings;
        this.audit = audit;
    }

    @Transactional
    public AccountPrincipal register(RegistrationRequest r) {
        if (!Boolean.TRUE.equals(r.acceptTerms()) || !Boolean.TRUE.equals(r.acceptPrivacy())
                || !Boolean.TRUE.equals(r.consentChildData())) {
            throw ApiException.field("consent-required", "consent",
                    "Please read and accept the terms, the privacy notice and the consent for your child's data.");
        }
        String email = r.parent().email().trim().toLowerCase(Locale.ROOT);
        policy.check(r.parent().password(), email, "parent.password");
        int taken = jdbc.sql("SELECT COUNT(*) FROM user_account WHERE email = :e").param("e", email)
                .query(Integer.class).single();
        if (taken > 0) {
            // A deliberate trade-off, documented in docs/03 DD-22: a clear message beats a silent failure here.
            throw ApiException.field("email-taken", "parent.email",
                    "An account with this email already exists. Please sign in instead.");
        }

        Instant now = Instant.now();
        jdbc.sql("""
                        INSERT INTO user_account (email, password_hash, role, status, failed_logins,
                                                  must_change_password, password_changed_at, created_at, updated_at)
                        VALUES (:email, :hash, 'PARENT', 'ACTIVE', 0, FALSE, :now, :now, :now)""")
                .param("email", email).param("hash", passwords.encode(r.parent().password())).param("now", now)
                .update();
        long accountId = jdbc.sql("SELECT id FROM user_account WHERE email = :e").param("e", email)
                .query(Long.class).single();
        jdbc.sql("""
                        INSERT INTO parent (account_id, full_name, mobile, city, created_at, updated_at)
                        VALUES (:a, :name, :mobile, :city, :now, :now)""")
                .param("a", accountId).param("name", r.parent().fullName().trim())
                .param("mobile", blankToNull(r.parent().mobile())).param("city", blankToNull(r.parent().city()))
                .param("now", now).update();
        long parentId = jdbc.sql("SELECT id FROM parent WHERE account_id = :a").param("a", accountId)
                .query(Long.class).single();

        String version = settings.stringValue(Settings.CONSENT_VERSION);
        for (String type : new String[] {"TERMS", "PRIVACY", "CHILD_DATA"}) {
            jdbc.sql("""
                            INSERT INTO consent_record (parent_id, consent_type, document_version, accepted_at)
                            VALUES (:p, :t, :v, :now)""")
                    .param("p", parentId).param("t", type).param("v", version).param("now", now).update();
        }

        ChildPart c = r.child();
        long childId = children.create(parentId,
                new ChildInput(c.firstName(), c.displayName(), c.dateOfBirth(), c.username(), c.avatarCode()));

        audit.record(accountId, Role.PARENT.name(), "ACCOUNT_REGISTERED", "user_account", accountId,
                Map.of("childId", childId, "consentVersion", version));
        return new AccountPrincipal(accountId, email, null, Role.PARENT, true, null, false);
    }

    private static String blankToNull(String s) {
        return s == null || s.isBlank() ? null : s.trim();
    }
}
