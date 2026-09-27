package org.clevercubs.content;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import com.jayway.jsonpath.JsonPath;

/**
 * The media library stays light (FUN-E29, FUN-E32; tools/optimize_media.py). Reads the files the application
 * serves ({@code clevercubs.media-root}, {@code ../media} beside {@code app/}) and the course JSON.
 */
class MediaWeightTests {

    private static final Path MEDIA = Path.of("..", "media");
    private static final Path CONTENT = Path.of("src", "main", "resources", "content");
    private static final long CARD_PICTURE_LIMIT = 100 * 1024;

    @Test
    @DisplayName("a picture on a lesson card (shown at 160 px) weighs at most 100 KB (FUN-E29)")
    void cardPicturesAreSmall() throws IOException {
        List<String> tooHeavy = new ArrayList<>();
        int checked = 0;
        try (Stream<Path> courses = Files.list(CONTENT)) {
            for (Path course : courses.filter(p -> p.toString().endsWith(".json")).toList()) {
                List<String> cards = JsonPath.read(course.toFile(),
                        "$.lessons[*].items[?(@.image != null && @.video == null)].image");
                for (String card : cards) {
                    long size = Files.size(MEDIA.resolve(card));
                    checked++;
                    if (size > CARD_PICTURE_LIMIT) tooHeavy.add(card + " (" + size / 1024 + " KB)");
                }
            }
        }
        assertThat(checked).as("card pictures found").isGreaterThan(50);
        assertThat(tooHeavy).as("card pictures over 100 KB; run tools/optimize_media.py").isEmpty();
    }

    @Test
    @DisplayName("every lesson sound and video has its index before its data, so playback starts at once (FUN-E32)")
    void soundAndVideoStartFast() throws IOException {
        List<String> slow = new ArrayList<>();
        int checked = 0;
        try (Stream<Path> files = Files.walk(MEDIA)) {
            for (Path file : files.filter(MediaWeightTests::isMp4).toList()) {
                List<String> boxes = topLevelBoxes(file);
                checked++;
                boolean indexLast = boxes.contains("moov") && boxes.contains("mdat")
                        && boxes.indexOf("mdat") < boxes.indexOf("moov");
                if (indexLast) slow.add(MEDIA.relativize(file).toString());
            }
        }
        assertThat(checked).as("MP4/M4A files found").isGreaterThan(100);
        assertThat(slow).as("index after the data; run tools/optimize_media.py").isEmpty();
    }

    private static boolean isMp4(Path p) {
        String name = p.getFileName().toString().toLowerCase();
        return name.endsWith(".mp4") || name.endsWith(".m4a");
    }

    /** The order of the top-level MP4 boxes (ftyp, moov, mdat, ...), read from their headers only. */
    static List<String> topLevelBoxes(Path file) throws IOException {
        List<String> boxes = new ArrayList<>();
        try (InputStream raw = Files.newInputStream(file); DataInputStream in = new DataInputStream(raw)) {
            while (true) {
                byte[] head = in.readNBytes(8);
                if (head.length < 8) break;
                long size = ((head[0] & 0xFFL) << 24) | ((head[1] & 0xFFL) << 16) | ((head[2] & 0xFFL) << 8) | (head[3] & 0xFFL);
                boxes.add(new String(head, 4, 4, StandardCharsets.ISO_8859_1));
                long header = 8;
                if (size == 1) {
                    size = in.readLong();
                    header = 16;
                }
                if (size == 0) break;
                in.skipNBytes(size - header);
            }
        }
        return boxes;
    }
}
