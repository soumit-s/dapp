package com.dapp.profileservice.kafka_listener;

import java.time.Duration;
import java.util.Set;
import java.util.UUID;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.test.context.EmbeddedKafka;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.bean.override.mockito.MockitoSpyBean;

import com.dapp.profileservice.common.entity.AdminProfile;
import com.dapp.profileservice.common.repository.AdminProfileRepository;
import com.dapp.profileservice.kafka_listener.listener.UserEventListener;
import com.dapp.profileservice.kafka_listener.model.UserCreatedEventDTO;
import com.dapp.profileservice.kafka_listener.model.UserCreatedPayloadDTO;
import com.dapp.profileservice.kafka_listener.model.UserRole;

import tools.jackson.databind.ObjectMapper;

import static org.awaitility.Awaitility.await;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

@SpringBootTest(classes = KafkaListenerApplication.class)
@DirtiesContext
@EmbeddedKafka
@ActiveProfiles("test")
public class UserEventHandlerIntegrationTest {

    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    @Autowired
    private AdminProfileRepository adminProfileRepository;

    @Autowired
    private ObjectMapper objectMapper;

    @MockitoSpyBean
    private UserEventListener userEventListener;

    @Test
    void testAdminCreatedEvent() throws Exception {
        UserCreatedPayloadDTO payload = new UserCreatedPayloadDTO();
        payload.setEmail("test@dapp.com");
        payload.setId(Long.valueOf(1));
        payload.setRole(Set.of(UserRole.ROLE_ADMIN));

        UserCreatedEventDTO event = new UserCreatedEventDTO();
        event.setEventType("user.created");
        event.setAggregateId(String.valueOf(1));
        event.setAggregateType("user");
        event.setEventId(UUID.randomUUID().toString());
        event.setPayload(payload);

        String rawJson = objectMapper.writeValueAsString(event);
        kafkaTemplate.send("outbox.user", rawJson);

        await().atMost(Duration.ofSeconds(2))
                .pollInterval(Duration.ofMillis(200))
                .until(() -> adminProfileRepository.findByUserId(payload.getId()).isPresent());
        verify(userEventListener, times(0)).handleUnknown(any(), any(), any());
        verify(userEventListener, times(1)).handleUserCreatedEvent(any());
        AdminProfile entity = adminProfileRepository.findByUserId(payload.getId()).orElseThrow(() -> new AssertionError(""));
        assertEquals(entity.getName(), payload.getEmail().substring(0, payload.getEmail().indexOf('@')));
        assertEquals(entity.getEmail(), payload.getEmail());
    }
}
