package org.clevercubs.quiz;

/**
 * Quiz scoring and the attempt rules (requirement section 11, D62-D64, docs/05 section 4). Pure; no Spring.
 */
public final class QuizRules {

    private QuizRules() {
    }

    /** {@code round(100 x correct / questions)}. */
    public static int scorePercent(int correct, int questions) {
        if (questions <= 0) {
            return 0;
        }
        return (int) Math.round(100.0 * Math.clamp(correct, 0, questions) / questions);
    }

    /** Passing means reaching the quiz's pass mark (70% by default, D62). */
    public static boolean passed(int scorePercent, int passMarkPercent) {
        return scorePercent >= passMarkPercent;
    }

    /** A reward needs a best score of the threshold or more (80%, compared with >=, D64). */
    public static boolean earnsReward(Integer bestScorePercent, int thresholdPercent) {
        return bestScorePercent != null && bestScorePercent >= thresholdPercent;
    }

    /** Locked: every allowed attempt is used, none is open, and the quiz was never passed (D63). */
    public static boolean locked(int attemptsUsed, int attemptsAllowed, boolean passed, boolean attemptOpen) {
        return !passed && !attemptOpen && attemptsUsed >= attemptsAllowed;
    }
}
