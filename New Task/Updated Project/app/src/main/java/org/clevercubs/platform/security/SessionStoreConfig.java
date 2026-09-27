package org.clevercubs.platform.security;

import java.util.Map;

import org.springframework.boot.autoconfigure.condition.ConditionalOnClass;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.web.context.HttpSessionSecurityContextRepository;
import org.springframework.session.FindByIndexNameSessionRepository;
import org.springframework.session.Session;
import org.springframework.session.config.SessionRepositoryCustomizer;
import org.springframework.session.jdbc.JdbcIndexedSessionRepository;

/**
 * Server sessions live in the database (Spring Session JDBC, tables from V4), so a sign-in survives a
 * restart and works when the host runs several instances or stops idle ones (D73). The session cookie
 * keeps its name and flags from {@code server.servlet.session.cookie}.
 *
 * <p>Spring Session indexes each session by the principal's name, which here would be the parent's email
 * address, in a plain searchable column. The index holds the account id instead. (The stored security
 * context itself is serialised with the signed-in account, as it is in memory; its password hash is erased.)
 */
@Configuration(proxyBeanMethods = false)
@ConditionalOnClass(JdbcIndexedSessionRepository.class)
class SessionStoreConfig {

    @Bean
    SessionRepositoryCustomizer<JdbcIndexedSessionRepository> indexSessionsByAccountId() {
        return repository -> repository.setIndexResolver(SessionStoreConfig::accountIndex);
    }

    static Map<String, String> accountIndex(Session session) {
        SecurityContext context = session.getAttribute(HttpSessionSecurityContextRepository.SPRING_SECURITY_CONTEXT_KEY);
        if (context != null && context.getAuthentication() instanceof SessionAuthentication signedIn) {
            return Map.of(FindByIndexNameSessionRepository.PRINCIPAL_NAME_INDEX_NAME,
                    Long.toString(signedIn.account().accountId()));
        }
        return Map.of();
    }
}
