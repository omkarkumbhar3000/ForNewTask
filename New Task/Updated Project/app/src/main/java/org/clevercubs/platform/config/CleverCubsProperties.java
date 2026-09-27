package org.clevercubs.platform.config;

import java.util.Arrays;
import java.util.List;
import java.util.regex.Pattern;

import org.springframework.boot.context.properties.ConfigurationProperties;

/**
 * Application settings bound from {@code clevercubs.*} in application.yml, which reads them from the
 * environment. Business rules that the Super Admin may change live in the {@code system_setting} table
 * instead (see {@link org.clevercubs.platform.settings.Settings}).
 *
 * @param mediaRoot    folder holding the course media, resolved against the working directory
 * @param contactEmail one or more addresses for the Contact Us page, separated by commas or semicolons
 *                     (CC_CONTACT_EMAIL, D80); empty shows that the address is being set up
 * @param admin        first Super Admin, created only when none exists
 */
@ConfigurationProperties(prefix = "clevercubs")
public record CleverCubsProperties(String mediaRoot, String contactEmail, Admin admin) {

    /** A plain shape check, enough to keep a typo or a stray word off the public page. */
    private static final Pattern ADDRESS = Pattern.compile("^[^@\\s,;]+@[^@\\s,;]+\\.[^@\\s,;]+$");

    public CleverCubsProperties {
        mediaRoot = (mediaRoot == null || mediaRoot.isBlank()) ? "../media" : mediaRoot;
        contactEmail = contactEmail == null ? "" : contactEmail.trim();
        admin = admin == null ? new Admin("", "") : admin;
    }

    /** The well-formed contact addresses, each once, in the order given. */
    public List<String> contactEmails() {
        return Arrays.stream(contactEmail.split("[,;]"))
                .map(String::trim)
                .filter(a -> ADDRESS.matcher(a).matches())
                .distinct()
                .toList();
    }

    public record Admin(String bootstrapEmail, String bootstrapPassword) {

        public Admin {
            bootstrapEmail = bootstrapEmail == null ? "" : bootstrapEmail.trim();
            bootstrapPassword = bootstrapPassword == null ? "" : bootstrapPassword;
        }

        /** Never print the password; this keeps it out of logs if the record is ever logged. */
        @Override
        public String toString() {
            return "Admin[bootstrapEmail=" + bootstrapEmail + ", bootstrapPassword=***]";
        }
    }
}
