package org.clevercubs.child;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.LocalDate;
import java.util.List;

import org.clevercubs.child.AgeGroups.AgeGroup;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** DD-08 username rules, D66 age groups and DD-06 avatars, without Spring. */
class ChildRulesTests {

    private static final List<AgeGroup> BANDS = List.of(
            new AgeGroup(1, "TINY", "Tiny Cubs", 2, 3, "TODDLER", 1),
            new AgeGroup(2, "LITTLE", "Little Cubs", 4, 5, "PRESCHOOL", 2),
            new AgeGroup(3, "BIG", "Big Cubs", 6, 8, "EARLY_PRIMARY", 3));

    @Test
    void ageIsWholeYears() {
        LocalDate today = LocalDate.of(2026, 9, 26);
        assertThat(AgeGroups.ageInYears(LocalDate.of(2022, 9, 27), today)).isEqualTo(3);
        assertThat(AgeGroups.ageInYears(LocalDate.of(2022, 9, 26), today)).isEqualTo(4);
    }

    @Test
    @DisplayName("each age falls in one band; older or younger children are served in the nearest band")
    void bands() {
        assertThat(AgeGroups.pick(BANDS, 2).code()).isEqualTo("TINY");
        assertThat(AgeGroups.pick(BANDS, 5).code()).isEqualTo("LITTLE");
        assertThat(AgeGroups.pick(BANDS, 8).code()).isEqualTo("BIG");
        assertThat(AgeGroups.pick(BANDS, 10).code()).isEqualTo("BIG");
        assertThat(AgeGroups.pick(BANDS, 1).code()).isEqualTo("TINY");
    }

    @Test
    void goodUsernames() {
        assertThat(UsernameRules.problem("happy-panda-12", "Zoe")).isEmpty();
        assertThat(UsernameRules.problem("class_owl", "Zoe")).as("'ass' inside a word is fine").isEmpty();
        assertThat(UsernameRules.problem(UsernameRules.suggest(), "Zoe")).isEmpty();
    }

    @Test
    void badUsernames() {
        assertThat(UsernameRules.problem("ab", "Zoe")).isPresent();
        assertThat(UsernameRules.problem("has space", "Zoe")).isPresent();
        assertThat(UsernameRules.problem("a@b.com", "Zoe")).isPresent();
        assertThat(UsernameRules.problem("zoe-rocks", "Zoe")).as("the real first name").isPresent();
        assertThat(UsernameRules.problem("call-9876543210", "Zoe")).as("phone-like").isPresent();
        assertThat(UsernameRules.problem("stupid-cat", "Zoe")).isPresent();
        assertThat(UsernameRules.problem("admin-bear", "Zoe")).isPresent();
    }

    @Test
    void avatarsAreAFixedSet() {
        assertThat(Avatars.isValid("owl")).isTrue();
        assertThat(Avatars.isValid("../../etc/passwd")).isFalse();
        assertThat(Avatars.all()).hasSize(12);
        assertThat(Avatars.emoji("nope")).isEqualTo("🐻");
    }
}
