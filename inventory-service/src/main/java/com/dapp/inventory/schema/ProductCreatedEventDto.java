package com.dapp.inventory.schema;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
public class ProductCreatedEventDto extends KafkaEventDto{
    ProductCreatedEventPayloadDto paylaod;
}
