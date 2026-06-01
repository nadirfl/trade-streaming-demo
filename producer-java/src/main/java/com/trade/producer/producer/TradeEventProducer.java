package com.trade.producer.producer;

import com.trade.producer.model.TradeEvent;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

@Service
public class TradeEventProducer {
    
    private final KafkaTemplate<String, TradeEvent> kafkaTemplate;
    private final String topic;

    public TradeEventProducer(
        KafkaTemplate<String, TradeEvent> kafkaTemplate,
        @Value("${app.kafka.topic}") String topic
    ) {
        this.kafkaTemplate = kafkaTemplate;
        this.topic = topic;
    }

    public void sendTradeEvent(TradeEvent event) {
        kafkaTemplate.send(topic, event.tradeId(), event);
        System.out.println("Sent trade event: " + event);
    }

}
