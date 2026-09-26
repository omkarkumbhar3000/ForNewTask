package org.clevercubs.platform.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

/**
 * Application settings bound from {@code clevercubs.*} in application.yml, which reads them from the
 * environment. Business rules that the Super Admin may change live in the {@code system_setting} table
 * instead (see {@link org.clevercubs.platform.settings.Settings}).
 *
 * @param mediaRoot    folder holding the course media, resolved against the working directory
 * @param contactEmail address shown on the Contact Us page; empty until supplied (INF-02)
 * @param admin        first Super Admin, created only when none exists
 */
@ConfigurationProperties(prefix = "clevercubs")
public record CleverCubsProperties(String mediaRoot, String contactEmail, Admin admin) {

    public CleverCubsProperties {
        mediaRoot = (mediaRoot == null || mediaRoot.isBlank()) ? "../media" : mediaRoot;
        contactEmail = contactEmail == null ? "" : contactEmail.trim();
        admin = admin == null ? new Admin("", "") : admin;
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
