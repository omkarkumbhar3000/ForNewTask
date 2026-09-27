package org.clevercubs.platform.security;

import java.util.Set;

import org.springframework.beans.factory.ObjectProvider;
import org.springframework.session.FindByIndexNameSessionRepository;
import org.springframework.session.Session;
import org.springframework.stereotype.Component;

/**
 * Ends every stored session of one account (SEC-R02). An account's status is checked only when it signs in,
 * so disabling it must also delete the sessions it already holds, or a disabled account stays signed in until
 * its sessions time out. The sessions are found through the account-id index that {@link SessionStoreConfig}
 * writes.
 *
 * <p>Without database sessions (the {@code test} profile, whose MockMvc sessions live in the test) there is
 * nothing stored to end, and this does nothing.
 */
@Component
public class AccountSessions {

    private final ObjectProvider<FindByIndexNameSessionRepository<? extends Session>> repository;

    AccountSessions(ObjectProvider<FindByIndexNameSessionRepository<? extends Session>> repository) {
        this.repository = repository;
    }

    /** Deletes the account's stored sessions and returns how many there were. */
    public int endAll(long accountId) {
        FindByIndexNameSessionRepository<? extends Session> sessions = repository.getIfAvailable();
        if (sessions == null) {
            return 0;
        }
        Set<String> ids = sessions.findByPrincipalName(Long.toString(accountId)).keySet();
        ids.forEach(sessions::deleteById);
        return ids.size();
    }
}
