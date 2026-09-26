package org.clevercubs.child;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.SequencedMap;

/**
 * The fixed set of illustrated avatars (DD-06). There is no photo upload at all, which keeps children's
 * photos out of the system and removes the unsafe-upload risk of requirement section 20.
 */
public final class Avatars {

    private static final SequencedMap<String, String> ALL = new LinkedHashMap<>();

    static {
        ALL.put("bear", "🐻");
        ALL.put("fox", "🦊");
        ALL.put("owl", "🦉");
        ALL.put("panda", "🐼");
        ALL.put("lion", "🦁");
        ALL.put("bunny", "🐰");
        ALL.put("cat", "🐱");
        ALL.put("dog", "🐶");
        ALL.put("frog", "🐸");
        ALL.put("koala", "🐨");
        ALL.put("penguin", "🐧");
        ALL.put("unicorn", "🦄");
    }

    private Avatars() {
    }

    public static boolean isValid(String code) {
        return code != null && ALL.containsKey(code);
    }

    public static String emoji(String code) {
        return ALL.getOrDefault(code, "🐻");
    }

    public static String defaultCode() {
        return "bear";
    }

    /** Every avatar, in display order: code to emoji. */
    public static Map<String, String> all() {
        return java.util.Collections.unmodifiableSequencedMap(ALL);
    }
}
