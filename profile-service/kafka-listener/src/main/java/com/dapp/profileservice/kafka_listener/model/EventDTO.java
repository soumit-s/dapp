package com.dapp.profileservice.kafka_listener.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonTypeInfo;

import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, include = JsonTypeInfo.As.PROPERTY, property = "event_type", visible = true)
@JsonSubTypes({
    @JsonSubTypes.Type(value = UserCreatedEventDTO.class, name = "user.created")
})
public abstract class EventDTO {
    @JsonProperty("event_id")
    @NotNull
    private String eventId;

    @JsonProperty("event_type")
    @NotNull
    private String eventType;
    
    @JsonProperty("aggregate_id")
    @NotNull
    private String aggregateId;
    
    @JsonProperty("aggregate_type")
    @NotNull
    private String aggregateType;
}
