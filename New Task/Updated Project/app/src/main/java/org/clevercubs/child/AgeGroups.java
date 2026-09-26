package org.clevercubs.child;

import java.time.LocalDate;
import java.time.Period;
import java.util.List;
import java.util.Optional;

import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Component;

/**
 * Age groups are data (D66: 2-3, 4-5, 6-8, editable by the Super Admin), and a child's group is always
 * derived from the date of birth, never stored, so it moves on with birthdays (docs/05 section 4).
 */
@Component
public class AgeGroups {

    public record AgeGroup(long id, String code, String name, int minAge, int maxAge, String uiProfile,
            int sortOrder) {

        boolean covers(int age) {
            return age >= minAge && age <= maxAge;
        }
    }

    private final JdbcClient jdbc;

    public AgeGroups(JdbcClient jdbc) {
        this.jdbc = jdbc;
    }

    public List<AgeGroup> all() {
        return jdbc.sql("""
                        SELECT id, code, name, min_age, max_age, ui_profile, sort_order
                        FROM age_group ORDER BY sort_order""")
                .query((rs, n) -> new AgeGroup(rs.getLong(1), rs.getString(2), rs.getString(3), rs.getInt(4),
                        rs.getInt(5), rs.getString(6), rs.getInt(7)))
                .list();
    }

    /** Whole years between the birthday and today. */
    public static int ageInYears(LocalDate dateOfBirth, LocalDate today) {
        return Period.between(dateOfBirth, today).getYears();
    }

    /** The group a newly registered child falls in; empty when the age is outside every configured band. */
    public Optional<AgeGroup> forNewChild(LocalDate dateOfBirth, LocalDate today) {
        int age = ageInYears(dateOfBirth, today);
        return all().stream().filter(g -> g.covers(age)).findFirst();
    }

    /**
     * The group an existing child is served in. A child who has grown past the oldest band stays in it, and
     * one younger than the first band is served as the youngest, so a registered child always has a group.
     */
    public AgeGroup forChild(LocalDate dateOfBirth, LocalDate today) {
        List<AgeGroup> groups = all();
        int age = ageInYears(dateOfBirth, today);
        return pick(groups, age);
    }

    static AgeGroup pick(List<AgeGroup> groups, int age) {
        if (groups.isEmpty()) {
            throw new IllegalStateException("No age groups are configured");
        }
        for (AgeGroup g : groups) {
            if (g.covers(age)) {
                return g;
            }
        }
        return age < groups.getFirst().minAge() ? groups.getFirst() : groups.getLast();
    }

    /** The youngest and oldest ages any band accepts, for the registration form and its message. */
    public int[] acceptedRange() {
        List<AgeGroup> groups = all();
        int min = groups.stream().mapToInt(AgeGroup::minAge).min().orElse(0);
        int max = groups.stream().mapToInt(AgeGroup::maxAge).max().orElse(0);
        return new int[] {min, max};
    }
}
