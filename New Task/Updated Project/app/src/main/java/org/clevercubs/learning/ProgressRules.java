package org.clevercubs.learning;

/**
 * Course progress (requirement section 10, D61, docs/05 section 4). Pure arithmetic, no Spring, no database.
 *
 * <ul>
 *   <li>A course with a required quiz: lessons are worth {@code lessonWeight}% (70 by default) and passing the
 *       quiz adds the rest. So a course never shows 100% before its quiz is passed.</li>
 *   <li>A course without a required quiz (rhymes, stories): its lessons are the whole 100%.</li>
 * </ul>
 *
 * Rounding is always down, so a partly finished course can never be rounded up to "complete".
 */
public final class ProgressRules {

    private ProgressRules() {
    }

    public static int coursePercent(boolean hasRequiredQuiz, int lessonsDone, int lessonsTotal, boolean quizPassed,
            int lessonWeight) {
        if (lessonsTotal <= 0) {
            return 0;
        }
        int done = Math.clamp(lessonsDone, 0, lessonsTotal);
        if (!hasRequiredQuiz) {
            return 100 * done / lessonsTotal;
        }
        int weight = Math.clamp(lessonWeight, 0, 100);
        int lessonPart = weight * done / lessonsTotal;
        int quizPart = quizPassed ? 100 - weight : 0;
        int percent = lessonPart + quizPart;
        // Belt and braces for the section 10 rule: 100% needs every lesson and the quiz.
        if (percent >= 100 && (done < lessonsTotal || !quizPassed)) {
            return 99;
        }
        return Math.min(percent, 100);
    }

    /** The overall progress of a set of courses: the plain average, rounded down. */
    public static int average(int... percents) {
        if (percents.length == 0) {
            return 0;
        }
        int sum = 0;
        for (int p : percents) {
            sum += p;
        }
        return sum / percents.length;
    }
}
