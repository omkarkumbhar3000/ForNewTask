package org.clevercubs.platform.web;

import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;

import org.clevercubs.platform.config.CleverCubsProperties;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.CacheControl;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.ViewControllerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * Clean page URLs and the course media library.
 *
 * <p>Pages are static HTML shells in {@code static/}; each area has an {@code index.html}. The media library
 * is a folder outside the jar ({@code clevercubs.media-root}, default {@code ../media}), served with byte
 * ranges so videos start at once, and with Spring's resource resolver, which rejects {@code ..}, encoded
 * traversal and absolute paths (requirement section 20, path traversal).
 */
@Configuration
class WebConfig implements WebMvcConfigurer {

    private static final Logger log = LoggerFactory.getLogger(WebConfig.class);

    private final Path mediaRoot;

    WebConfig(CleverCubsProperties properties) {
        this.mediaRoot = Path.of(properties.mediaRoot()).toAbsolutePath().normalize();
        if (!Files.isDirectory(mediaRoot)) {
            log.warn("Media folder {} does not exist; lesson pictures, sounds and videos will not load",
                    mediaRoot);
        }
    }

    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        registry.addViewController("/").setViewName("forward:/index.html");
        registry.addViewController("/login").setViewName("forward:/login.html");
        registry.addViewController("/register").setViewName("forward:/register.html");
        registry.addViewController("/terms").setViewName("forward:/terms.html");
        registry.addViewController("/privacy").setViewName("forward:/privacy.html");
        registry.addViewController("/contact").setViewName("forward:/contact.html");
        for (String area : new String[] {"parent", "learn", "admin"}) {
            registry.addViewController("/" + area).setViewName("redirect:/" + area + "/");
            registry.addViewController("/" + area + "/").setViewName("forward:/" + area + "/index.html");
        }
    }

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        String location = mediaRoot.toUri().toString();
        registry.addResourceHandler("/media/**")
                .addResourceLocations(location.endsWith("/") ? location : location + "/")
                .setCacheControl(CacheControl.maxAge(Duration.ofDays(7)).cachePrivate());
    }
}
