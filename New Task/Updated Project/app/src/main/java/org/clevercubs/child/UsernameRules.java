package org.clevercubs.child;

import java.security.SecureRandom;
import java.util.List;
import java.util.Locale;
import java.util.Optional;
import java.util.regex.Pattern;

/**
 * The safety rules for a child's username (DD-08, requirement section 12): 3 to 20 letters, digits, hyphens
 * or underscores; nothing that looks like a phone number or an email address; not the child's own first
 * name; and nothing from a small blocked-words list. Suggestions are friendly word pairs such as
 * {@code happy-panda-12}, so a parent never has to invent one. Pure rules: no Spring, no database.
 */
public final class UsernameRules {

    private static final Pattern SHAPE = Pattern.compile("^[A-Za-z0-9_-]{3,20}$");
    private static final Pattern PHONE_LIKE = Pattern.compile("\\d{6,}");
    private static final List<String> BLOCKED = List.of(
            "admin", "root", "support", "clevercubs", "moderator", "staff", "teacher", "official",
            "sex", "porn", "nude", "kill", "die", "dead", "hate", "stupid", "idiot", "dumb", "ugly", "fat",
            "drug", "weed", "beer", "gun", "shit", "fuck", "damn", "crap", "ass", "bitch", "bastard");

    private static final String[] ADJECTIVES = {
        "happy", "brave", "sunny", "clever", "kind", "bright", "gentle", "jolly", "lucky", "merry", "swift",
        "curious", "cheery", "calm", "bouncy", "cosy", "super", "starry", "rainbow", "little"};
    private static final String[] ANIMALS = {
        "panda", "tiger", "koala", "otter", "owl", "fox", "bear", "bunny", "puppy", "kitten", "lion", "zebra",
        "dolphin", "penguin", "robin", "turtle", "giraffe", "hippo", "lamb", "seal"};

    private static final SecureRandom RANDOM = new SecureRandom();

    private UsernameRules() {
    }

    /** Why the username cannot be used, in words a parent can act on; empty when it is fine. */
    public static Optional<String> problem(String username, String firstName) {
        if (username == null || !SHAPE.matcher(username).matches()) {
            return Optional.of("Use 3 to 20 letters, numbers, - or _.");
        }
        if (PHONE_LIKE.matcher(username).find()) {
            return Optional.of("Please don't use long numbers - they can look like a phone number.");
        }
        String lower = username.toLowerCase(Locale.ROOT);
        if (firstName != null) {
            String name = firstName.trim().toLowerCase(Locale.ROOT);
            if (name.length() >= 3 && lower.contains(name)) {
                return Optional.of("To keep your child private, please don't use their real name.");
            }
        }
        for (String word : BLOCKED) {
            if (lower.contains(word) && isWordLike(lower, word)) {
                return Optional.of("Please choose a different username.");
            }
        }
        return Optional.empty();
    }

    /** A random, friendly suggestion. The caller checks it is still free. */
    public static String suggest() {
        return ADJECTIVES[RANDOM.nextInt(ADJECTIVES.length)] + "-" + ANIMALS[RANDOM.nextInt(ANIMALS.length)]
                + "-" + (10 + RANDOM.nextInt(90));
    }

    /**
     * Short blocked words ("ass", "die") are refused only as a whole part of the name, so "class-owl" or
     * "diesel" stay usable; longer ones are refused anywhere.
     */
    private static boolean isWordLike(String username, String word) {
        if (word.length() > 4) {
            return true;
        }
        for (String part : username.split("[-_0-9]+")) {
            if (part.equals(word)) {
                return true;
            }
        }
        return false;
    }
}
