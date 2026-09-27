package org.clevercubs.platform.config;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** CC_CONTACT_EMAIL may hold several addresses (D80); only well-formed ones reach the Contact page. */
class CleverCubsPropertiesTests {

    private static CleverCubsProperties withContact(String value) {
        return new CleverCubsProperties("../media", value, null);
    }

    @Test
    @DisplayName("a comma- or semicolon-separated list gives each address once, in order")
    void severalAddresses() {
        assertThat(withContact(" first@example.test, second@example.test ; first@example.test ").contactEmails())
                .containsExactly("first@example.test", "second@example.test");
    }

    @Test
    @DisplayName("one address still works, and empty or malformed values show nothing")
    void singleEmptyAndMalformed() {
        assertThat(withContact("hello@example.test").contactEmails()).containsExactly("hello@example.test");
        assertThat(withContact("").contactEmails()).isEmpty();
        assertThat(withContact(null).contactEmails()).isEmpty();
        assertThat(withContact("not-an-address, also wrong@, ok@example.test").contactEmails())
                .containsExactly("ok@example.test");
    }
}
