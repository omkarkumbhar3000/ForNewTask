package org.clevercubs.child;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.List;
import java.util.Optional;

import org.clevercubs.child.AgeGroups.AgeGroup;
import org.clevercubs.platform.db.SqlDialect;
import org.clevercubs.platform.db.Timestamps;
import org.clevercubs.platform.web.ApiException;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Child profiles: creation (at registration or later by the parent), updates, ownership and the age-group
 * view of a child. A child never has a login (D58); every lookup here is scoped to the parent's account, and
 * a child that is not the caller's is reported as not found, so its existence is not revealed.
 */
@Service
public class ChildService {

    public record ChildInput(String firstName, String displayName, LocalDate dateOfBirth, String username,
            String avatarCode) {
    }

    public record ChildUpdate(String displayName, String username, String avatarCode, LocalDate dateOfBirth,
            Boolean soundEffects, Boolean readAloud) {
    }

    public record ChildRow(long id, long parentId, String firstName, String displayName, String username,
            LocalDate dateOfBirth, String avatarCode, boolean soundEffects, boolean readAloud) {
    }

    /** What the pages show about a child. Date of birth only goes to the parent's own views. */
    public record ChildView(long id, String firstName, String displayName, String username, String avatarCode,
            String avatar, String ageGroupCode, String ageGroupName, String uiProfile, int age,
            LocalDate dateOfBirth, boolean soundEffects, boolean readAloud) {
    }

    private static final String SELECT = """
            SELECT id, parent_id, first_name, display_name, username, date_of_birth, avatar_code,
                   sound_effects, read_aloud
            FROM child""";

    private final JdbcClient jdbc;
    private final SqlDialect dialect;
    private final AgeGroups ageGroups;

    public ChildService(JdbcClient jdbc, AgeGroups ageGroups, SqlDialect dialect) {
        this.jdbc = jdbc;
        this.ageGroups = ageGroups;
        this.dialect = dialect;
    }

    @Transactional
    public long create(long parentId, ChildInput in) {
        String firstName = required(in.firstName(), "firstName", 40, "Please enter the child's first name.");
        String displayName = optional(in.displayName(), "displayName", 40);
        if (displayName == null) {
            displayName = firstName;
        }
        LocalDate today = today();
        AgeGroup group = acceptedGroup(in.dateOfBirth(), today);

        String username = blank(in.username()) ? freeSuggestion(firstName) : in.username().trim();
        checkUsername(username, firstName, null);
        String avatar = Avatars.isValid(in.avatarCode()) ? in.avatarCode() : Avatars.defaultCode();

        LocalDateTime now = Timestamps.now();
        jdbc.sql("""
                        INSERT INTO child (parent_id, first_name, display_name, username, date_of_birth, avatar_code,
                                           created_at, updated_at)
                        VALUES (:parent, :first, :display, :username, :dob, :avatar, :now, :now)""")
                .param("parent", parentId)
                .param("first", firstName)
                .param("display", displayName)
                .param("username", username)
                .param("dob", in.dateOfBirth())
                .param("avatar", avatar)
                .param("now", now)
                .update();
        long childId = jdbc.sql("SELECT id FROM child WHERE username = " + dialect.caseInsensitive("u"))
                .param("u", username)
                .query(Long.class).single();
        enrolInYearOne(childId, group.id());
        return childId;
    }

    @Transactional
    public void update(long childId, ChildUpdate u) {
        ChildRow current = find(childId).orElseThrow(() -> ApiException.notFound("Child"));
        String displayName = u.displayName() == null ? current.displayName()
                : required(u.displayName(), "displayName", 40, "Please enter a display name.");
        String username = current.username();
        if (u.username() != null && !u.username().trim().equalsIgnoreCase(current.username())) {
            username = u.username().trim();
            checkUsername(username, current.firstName(), childId);
        }
        String avatar = u.avatarCode() == null ? current.avatarCode() : u.avatarCode();
        if (!Avatars.isValid(avatar)) {
            throw ApiException.field("invalid-input", "avatarCode", "Please pick one of the avatars.");
        }
        LocalDate dob = current.dateOfBirth();
        if (u.dateOfBirth() != null && !u.dateOfBirth().equals(dob)) {
            dob = u.dateOfBirth();
            acceptedGroup(dob, today());
        }
        jdbc.sql("""
                        UPDATE child SET display_name = :display, username = :username, avatar_code = :avatar,
                               date_of_birth = :dob, sound_effects = :sound, read_aloud = :read,
                               updated_at = :now
                        WHERE id = :id""")
                .param("display", displayName)
                .param("username", username)
                .param("avatar", avatar)
                .param("dob", dob)
                .param("sound", u.soundEffects() == null ? current.soundEffects() : u.soundEffects())
                .param("read", u.readAloud() == null ? current.readAloud() : u.readAloud())
                .param("now", Timestamps.now())
                .param("id", childId)
                .update();
    }

    /** Applies a username the parent approved from a child's request; the same rules apply. */
    @Transactional
    public void changeUsername(long childId, String username) {
        update(childId, new ChildUpdate(null, username, null, null, null, null));
    }

    public Optional<ChildRow> find(long childId) {
        return jdbc.sql(SELECT + " WHERE id = :id").param("id", childId).query(ChildService::row).optional();
    }

    /** The child, if it belongs to this parent account; otherwise not found (never "forbidden"). */
    public ChildRow requireOwned(long accountId, long childId) {
        return jdbc.sql(SELECT + " WHERE id = :id AND parent_id = (SELECT id FROM parent WHERE account_id = :a)")
                .param("id", childId)
                .param("a", accountId)
                .query(ChildService::row)
                .optional()
                .orElseThrow(() -> ApiException.notFound("Child"));
    }

    public List<ChildRow> forAccount(long accountId) {
        return jdbc.sql(SELECT + " WHERE parent_id = (SELECT id FROM parent WHERE account_id = :a) ORDER BY id")
                .param("a", accountId)
                .query(ChildService::row)
                .list();
    }

    public Optional<Long> parentIdOf(long accountId) {
        return jdbc.sql("SELECT id FROM parent WHERE account_id = :a").param("a", accountId)
                .query(Long.class).optional();
    }

    public AgeGroup groupOf(ChildRow child) {
        return ageGroups.forChild(child.dateOfBirth(), today());
    }

    public ChildView view(ChildRow c) {
        AgeGroup g = groupOf(c);
        return new ChildView(c.id(), c.firstName(), c.displayName(), c.username(), c.avatarCode(),
                Avatars.emoji(c.avatarCode()), g.code(), g.name(), g.uiProfile(),
                AgeGroups.ageInYears(c.dateOfBirth(), today()), c.dateOfBirth(), c.soundEffects(), c.readAloud());
    }

    public boolean isUsernameFree(String username, Long exceptChildId) {
        return jdbc.sql("SELECT COUNT(*) FROM child WHERE username = " + dialect.caseInsensitive("u")
                        + " AND id <> :except")
                .param("u", username)
                .param("except", exceptChildId == null ? -1L : exceptChildId)
                .query(Integer.class).single() == 0;
    }

    public String freeSuggestion() {
        return freeSuggestion(null);
    }

    /** A free suggestion that also passes the rules for this child, e.g. never "happy-kitten-12" for Kit. */
    public String freeSuggestion(String firstName) {
        for (int i = 0; i < 50; i++) {
            String candidate = UsernameRules.suggest();
            if (UsernameRules.problem(candidate, firstName).isEmpty() && isUsernameFree(candidate, null)) {
                return candidate;
            }
        }
        throw new IllegalStateException("Could not find a free username");
    }

    /** Enrols the child in the Year-1 program of their age group, if one is published (D65). */
    public void enrolInYearOne(long childId, long ageGroupId) {
        jdbc.sql(dialect.insertIgnoringDuplicates("""
                        INSERT INTO program_enrolment (child_id, program_id, status, started_at)
                        SELECT :child, id, 'ACTIVE', :now FROM program
                        WHERE age_group_id = :group AND year_number = 1 AND status = 'PUBLISHED'"""))
                .param("child", childId)
                .param("group", ageGroupId)
                .param("now", Timestamps.now())
                .update();
    }

    private AgeGroup acceptedGroup(LocalDate dob, LocalDate today) {
        if (dob == null) {
            throw ApiException.field("invalid-input", "dateOfBirth", "Please enter the date of birth.");
        }
        if (dob.isAfter(today)) {
            throw ApiException.field("invalid-input", "dateOfBirth", "The date of birth is in the future.");
        }
        return ageGroups.forNewChild(dob, today).orElseThrow(() -> {
            int[] range = ageGroups.acceptedRange();
            return ApiException.field("age-not-supported", "dateOfBirth",
                    "CleverCubs is made for children aged " + range[0] + " to " + range[1] + ".");
        });
    }

    private void checkUsername(String username, String firstName, Long exceptChildId) {
        UsernameRules.problem(username, firstName).ifPresent(message -> {
            throw ApiException.field("invalid-username", "username", message);
        });
        if (!isUsernameFree(username, exceptChildId)) {
            throw ApiException.field("username-taken", "username", "That username is taken. Try another one.");
        }
    }

    private static String required(String value, String field, int max, String message) {
        String v = optional(value, field, max);
        if (v == null) {
            throw ApiException.field("invalid-input", field, message);
        }
        return v;
    }

    private static String optional(String value, String field, int max) {
        if (value == null || value.isBlank()) {
            return null;
        }
        String v = value.trim();
        if (v.length() > max) {
            throw ApiException.field("invalid-input", field, "Please use at most " + max + " characters.");
        }
        return v;
    }

    private static boolean blank(String s) {
        return s == null || s.isBlank();
    }

    static LocalDate today() {
        return LocalDate.now(ZoneOffset.UTC);
    }

    private static ChildRow row(java.sql.ResultSet rs, int n) throws java.sql.SQLException {
        return new ChildRow(rs.getLong("id"), rs.getLong("parent_id"), rs.getString("first_name"),
                rs.getString("display_name"), rs.getString("username"),
                rs.getObject("date_of_birth", LocalDate.class), rs.getString("avatar_code"),
                rs.getBoolean("sound_effects"), rs.getBoolean("read_aloud"));
    }
}
