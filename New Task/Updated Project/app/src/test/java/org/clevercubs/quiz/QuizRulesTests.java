package org.clevercubs.quiz;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** D62 (pass at 70%), D63 (lock), D64 (reward at 80% or more). */
class QuizRulesTests {

    @Test
    void scoreIsRoundedPercent() {
        assertThat(QuizRules.scorePercent(7, 10)).isEqualTo(70);
        assertThat(QuizRules.scorePercent(2, 3)).isEqualTo(67);
        assertThat(QuizRules.scorePercent(0, 0)).isZero();
    }

    @Test
    void passMarkIsInclusive() {
        assertThat(QuizRules.passed(70, 70)).isTrue();
        assertThat(QuizRules.passed(69, 70)).isFalse();
    }

    @Test
    @DisplayName("the reward line is 80% or more: 8 of 10 and 4 of 5 earn it, 7 of 10 does not")
    void rewardThreshold() {
        assertThat(QuizRules.earnsReward(QuizRules.scorePercent(8, 10), 80)).isTrue();
        assertThat(QuizRules.earnsReward(QuizRules.scorePercent(4, 5), 80)).isTrue();
        assertThat(QuizRules.earnsReward(QuizRules.scorePercent(7, 10), 80)).isFalse();
        assertThat(QuizRules.earnsReward(null, 80)).isFalse();
    }

    @Test
    @DisplayName("locked only with every attempt used, none open, and no pass")
    void lock() {
        assertThat(QuizRules.locked(3, 3, false, false)).isTrue();
        assertThat(QuizRules.locked(3, 3, true, false)).isFalse();
        assertThat(QuizRules.locked(3, 3, false, true)).isFalse();
        assertThat(QuizRules.locked(2, 3, false, false)).isFalse();
        assertThat(QuizRules.locked(3, 6, false, false)).as("after a parent's grant").isFalse();
    }
}
