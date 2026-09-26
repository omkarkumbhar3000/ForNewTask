package org.clevercubs.learning;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

/** D61 and requirement section 10, as pure arithmetic. */
class ProgressRulesTests {

    @ParameterizedTest(name = "{1} of {2} lessons, quiz passed {3} -> {4}%")
    @CsvSource({
        "true, 0, 5, false, 0",
        "true, 1, 5, false, 14",
        "true, 3, 5, false, 42",
        "true, 5, 5, false, 70",
        "true, 5, 5, true, 100",
        "true, 2, 3, false, 46",
        "false, 0, 9, false, 0",
        "false, 3, 9, false, 33",
        "false, 9, 9, false, 100",
    })
    void coursePercent(boolean quiz, int done, int total, boolean passed, int expected) {
        assertThat(ProgressRules.coursePercent(quiz, done, total, passed, 70)).isEqualTo(expected);
    }

    @Test
    @DisplayName("a required quiz means never 100% before it is passed, whatever the weight")
    void neverCompleteWithoutTheQuiz() {
        for (int weight = 0; weight <= 100; weight += 5) {
            assertThat(ProgressRules.coursePercent(true, 4, 4, false, weight)).isLessThan(100);
            assertThat(ProgressRules.coursePercent(true, 3, 4, true, weight)).isLessThan(100);
        }
    }

    @Test
    @DisplayName("a course with no countable lessons is 0%, not a division by zero")
    void emptyCourse() {
        assertThat(ProgressRules.coursePercent(true, 0, 0, true, 70)).isZero();
    }

    @Test
    void averageRoundsDown() {
        assertThat(ProgressRules.average(100, 100, 99)).isEqualTo(99);
        assertThat(ProgressRules.average()).isZero();
    }
}
