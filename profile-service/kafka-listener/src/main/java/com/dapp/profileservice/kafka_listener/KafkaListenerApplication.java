package com.dapp.profileservice.kafka_listener;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.persistence.autoconfigure.EntityScan;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@SpringBootApplication
@ComponentScan(basePackages = "com.dapp.profileservice")
@EnableJpaRepositories(basePackages = "com.dapp.profileservice.common.repository")
@EntityScan(basePackages = "com.dapp.profileservice.common.entity")
public class KafkaListenerApplication {

	public static void main(String[] args) {
		SpringApplication.run(KafkaListenerApplication.class, args);
	}

}
