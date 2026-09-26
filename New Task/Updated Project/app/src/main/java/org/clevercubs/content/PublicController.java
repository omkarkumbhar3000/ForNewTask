package org.clevercubs.content;

import java.util.List;
import java.util.Map;

import org.clevercubs.child.AgeGroups;
import org.clevercubs.child.Avatars;
import org.clevercubs.child.ChildService;
import org.clevercubs.platform.config.CleverCubsProperties;
import org.clevercubs.platform.security.SessionAuthentication;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * What anyone may read before signing in: the course catalogue (no progress, no media), the contact address
 * (requirement section 17, INF-02), the avatars, the supported ages and a username suggestion for the
 * registration form.
 */
@RestController
@RequestMapping("/api/v1/public")
class PublicController {

    record CatalogueCourse(long id, String slug, String title, String description, String icon, String kind,
            int lessons, boolean hasQuiz) {
    }

    record AgeBand(String name, int minAge, int maxAge) {
    }

    private final JdbcClient jdbc;
    private final CleverCubsProperties properties;
    private final AgeGroups ageGroups;
    private final ChildService children;

    PublicController(JdbcClient jdbc, CleverCubsProperties properties, AgeGroups ageGroups, ChildService children) {
        this.jdbc = jdbc;
        this.properties = properties;
        this.ageGroups = ageGroups;
        this.children = children;
    }

    @GetMapping("/courses")
    List<CatalogueCourse> courses() {
        return jdbc.sql("""
                        SELECT c.id, c.slug, c.title, c.description, c.icon, c.kind,
                               (SELECT COUNT(*) FROM lesson l WHERE l.course_id = c.id AND l.status = 'PUBLISHED'),
                               EXISTS (SELECT 1 FROM quiz q WHERE q.course_id = c.id AND q.status = 'PUBLISHED')
                        FROM course c WHERE c.status = 'PUBLISHED' ORDER BY c.sort_order""")
                .query((rs, n) -> new CatalogueCourse(rs.getLong(1), rs.getString(2), rs.getString(3),
                        rs.getString(4), rs.getString(5), rs.getString(6), rs.getInt(7), rs.getBoolean(8)))
                .list();
    }

    @GetMapping("/contact")
    Map<String, Object> contact() {
        String email = properties.contactEmail();
        return Map.of("email", email == null ? "" : email, "configured", email != null && !email.isBlank());
    }

    @GetMapping("/avatars")
    Map<String, String> avatars() {
        return Avatars.all();
    }

    @GetMapping("/ages")
    Map<String, Object> ages() {
        int[] range = ageGroups.acceptedRange();
        List<AgeBand> bands = ageGroups.all().stream().map(g -> new AgeBand(g.name(), g.minAge(), g.maxAge())).toList();
        return Map.of("minAge", range[0], "maxAge", range[1], "groups", bands);
    }

    /**
     * Who the browser is signed in as, or {@code signedIn: false}. Public so that pages can shape their header
     * without an expected 401 on every visit; it reveals nothing a caller does not already hold (its own
     * session), and the same fields as {@code GET /api/v1/auth/me}.
     */
    @GetMapping("/session")
    Map<String, Object> session() {
        if (SecurityContextHolder.getContext().getAuthentication() instanceof SessionAuthentication s
                && s.isAuthenticated()) {
            Map<String, Object> m = new java.util.LinkedHashMap<>();
            m.put("signedIn", true);
            m.put("accountId", s.account().accountId());
            // A child's session never carries the parent's contact details (requirement section 7).
            if (s.mode() != org.clevercubs.platform.security.Role.CHILD) {
                m.put("email", s.account().email());
            }
            m.put("role", s.account().role().name());
            m.put("mode", s.mode().name());
            m.put("activeChildId", s.activeChildId());
            m.put("mustChangePassword", s.account().mustChangePassword());
            return m;
        }
        return Map.of("signedIn", false);
    }

    @GetMapping("/username-suggestion")
    Map<String, String> usernameSuggestion() {
        return Map.of("username", children.freeSuggestion());
    }
}
