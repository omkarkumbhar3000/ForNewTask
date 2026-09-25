/**
 * A 30-line hash router.
 *
 * Deliberately not react-router: the app has six views and one parameterised
 * route, so a dependency would cost more than it gives. Hash routing also means
 * the built `dist/` opens from the filesystem with no server rewrite rules.
 *
 * Routes:  #/            #/benchmark     #/history
 *          #/projects    #/findings      #/report/<runId>
 */
import { useEffect, useState } from 'react'

export function parseHash(hash) {
  const raw = String(hash || '').replace(/^#\/?/, '')
  const [path, ...rest] = raw.split('/')
  return { view: path || 'dashboard', param: rest.join('/') || null }
}

export function useRoute() {
  const [route, setRoute] = useState(() => parseHash(window.location.hash))

  useEffect(() => {
    const onChange = () => {
      setRoute(parseHash(window.location.hash))
      window.scrollTo({ top: 0, behavior: 'instant' })
    }
    window.addEventListener('hashchange', onChange)
    return () => window.removeEventListener('hashchange', onChange)
  }, [])

  return route
}

export function navigate(to) {
  const next = to.startsWith('#') ? to : `#/${to.replace(/^\//, '')}`
  if (window.location.hash === next) return
  window.location.hash = next
}
