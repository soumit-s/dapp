package com.dapp.profileservice.kafka_listener.listener;

import org.springframework.kafka.support.Acknowledgment;
import org.springframework.kafka.support.KafkaHeaders;
import org.springframework.kafka.support.serializer.FailedDeserializationInfo;
import org.springframework.messaging.Message;
import org.springframework.stereotype.Component;

import com.dapp.profileservice.common.exception.DuplicateAdminProfileExcetion;
import com.dapp.profileservice.common.model.AdminProfileDTO;
import com.dapp.profileservice.common.model.CreateAdminProfileDTO;
import com.dapp.profileservice.common.service.ProfileService;
import com.dapp.profileservice.kafka_listener.model.UserCreatedEventDTO;
import com.dapp.profileservice.kafka_listener.model.UserCreatedPayloadDTO;
import com.dapp.profileservice.kafka_listener.model.UserRole;

import lombok.extern.slf4j.Slf4j;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.kafka.annotation.KafkaHandler;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.listener.adapter.ConsumerRecordMetadata;

@Slf4j
@KafkaListener(id = "user-event-handler", groupId = "profile-service.user-event-listener-group", concurrency = "3", topics = "outbox.user")
@Component
public class UserEventListener {

    private final ProfileService profileService;

    public UserEventListener(ProfileService profileService) {
        this.profileService = profileService;
    }
    
    @KafkaHandler
    public void handleUserCreatedEvent(UserCreatedEventDTO event) {
        try {
            UserCreatedPayloadDTO payload = event.getPayload();
            if (payload.getRole().contains(UserRole.ROLE_USER)) {
                throw new UnsupportedOperationException("Unable to handle user created event for ROLE_USER");
            }

            try {
                if (payload.getRole().contains(UserRole.ROLE_ADMIN)) {
                    CreateAdminProfileDTO dto = new CreateAdminProfileDTO();
                    // Set the email suffix as the default name.
                    String email = payload.getEmail();
                    if (email.indexOf('@') != -1) {
                        dto.setName(email.substring(0, email.indexOf('@')));
                    } else {
                        dto.setName(email);
                    }
                    dto.setEmail(email);
                    dto.setUserId(payload.getId());
                    // Create the admin user.
                    AdminProfileDTO adminProfile = profileService.createAdminProfile(dto);
                    log.debug("Created admin profile: {}", adminProfile);
                }
            } catch (DuplicateAdminProfileExcetion e) {
                // Catch DuplicateAdminProfileException to maintain consistency in case of
                // duplicate reads or replays of partially executed or fully executed
                // user created events.

                // Just log the exception and forget.
                log.error("Admin profile already created for userId: {} {}", payload.getId(), e);;
            }
        } catch (Exception e) {
            // Push to Dead letter queue.
        }
    }

    // Poison Pill handler
    @KafkaHandler(isDefault = true)
    public void handleUnknown(Message<?> message, ConsumerRecordMetadata metadata, Acknowledgment ack) {
        Object payload=message.getPayload();
        if (payload instanceof FailedDeserializationInfo failedInfo) {
            byte[] rawBytes = failedInfo.getData();
            if (rawBytes == null) {
                String raw = new String(rawBytes);
                log.error("Malformed json message: {}", raw);
            } else {
                log.error("Malformed message with no data");
            }
        } else {
            ConsumerRecord<?, ?> record = message.getHeaders().get(KafkaHeaders.RAW_DATA,ConsumerRecord.class);
            if (record != null && record.value() != null) {
                String rawJson;
                if (record.value() instanceof byte[] rawBytes) {
                    rawJson=new String(rawBytes);
                } else {
                    rawJson = record.value().toString();
                }
                log.error("Unknown json message: {}", rawJson);
            } else {

            }
        }
    }
}
