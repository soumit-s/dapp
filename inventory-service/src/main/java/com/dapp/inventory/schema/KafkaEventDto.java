package com.dapp.inventory.schema;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonTypeInfo;

import lombok.Data;

@Data
@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, include=JsonTypeInfo.As.PROPERTY, property = "event_type", visible = true)
@JsonSubTypes({
    @JsonSubTypes.Type(value = StoreCreatedEventDto.class, name="store.created"),
    @JsonSubTypes.Type(value = ProductCreatedEventDto.class, name="product.created")
})
public abstract class KafkaEventDto {
    @JsonProperty("event_type")
    private String eventType;

    @JsonProperty("aggregate_type")
    private String aggregateType;

    @JsonProperty("aggregate_id")
    private String aggregateId;   
}
