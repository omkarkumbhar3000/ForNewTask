package org.clevercubs.platform.security;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.util.HashSet;
import java.util.Locale;
import java.util.Optional;
import java.util.Set;

import org.clevercubs.platform.web.ApiException;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Component;

/**
 * The one password rule for every path that sets a password (DD-01, NIST SP 800-63B): at least 12 characters,
 * not a well-known password, and not built from the account's own email address. No composition rules.
 * Registration, the password change and the admin bootstrap all ask this class, so the rule cannot drift.
 */
@Component
public class PasswordPolicy {

    public static final int MINIMUM_LENGTH = 12;
    public static final int MAXIMUM_LENGTH = 200;

    private final Set<String> common;

    public PasswordPolicy() {
        this.common = load("security/common-passwords.txt");
    }

    /** Why the password is not acceptable, in words a parent can act on; empty when it is fine. */
    public Optional<String> problem(String password, String email) {
        if (password == null || password.length() < MINIMUM_LENGTH) {
            return Optional.of("Use at least " + MINIMUM_LENGTH + " characters. A short sentence works well.");
        }
        if (password.length() > MAXIMUM_LENGTH) {
            return Optional.of("Use at most " + MAXIMUM_LENGTH + " characters.");
        }
        String lower = password.toLowerCase(Locale.ROOT);
        String letters = lower.replaceAll("[^a-z]", "");
        boolean commonWithDecoration = letters.length() >= 4 && common.contains(letters)
                && letters.length() * 2 >= lower.length();
        if (common.contains(lower) || commonWithDecoration || password.chars().distinct().count() <= 3
                || lower.matches("\\d+") || isSequence(lower)) {
            return Optional.of("This password is too easy to guess. Try a short sentence instead.");
        }
        if (lower.contains("clevercubs")) {
            return Optional.of("Please don't use the name of the app in your password.");
        }
        if (email != null) {
            int at = email.indexOf('@');
            String local = (at > 0 ? email.substring(0, at) : email).toLowerCase(Locale.ROOT);
            if (local.length() >= 4 && lower.contains(local)) {
                return Optional.of("Please don't use your email address in your password.");
            }
        }
        return Optional.empty();
    }

    /** Throws the problem as a {@code weak-password} answer, naming the field it belongs to. */
    public void check(String password, String email, String field) {
        problem(password, email).ifPresent(message -> {
            throw ApiException.field("weak-password", field, message);
        });
    }

    /** Runs such as "abcdefghijkl" or "123456789012": most steps go one character up or down. */
    static boolean isSequence(String s) {
        int steps = s.length() - 1;
        int runs = 0;
        for (int i = 1; i < s.length(); i++) {
            int d = s.charAt(i) - s.charAt(i - 1);
            if (d == 1 || d == -1 || d == 0) {
                runs++;
            }
        }
        return steps > 0 && runs * 4 >= steps * 3;
    }

    private static Set<String> load(String path) {
        Set<String> words = new HashSet<>();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(
                new ClassPathResource(path).getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String word = line.trim().toLowerCase(Locale.ROOT);
                if (!word.isEmpty() && !word.startsWith("#")) {
                    words.add(word);
                }
            }
        } catch (IOException e) {
            throw new UncheckedIOException("Cannot read " + path, e);
        }
        return Set.copyOf(words);
    }
}
