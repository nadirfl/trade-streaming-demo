package com.trade.producer.scheduler;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.Instant;
import java.util.List;
import java.util.Random;
import java.util.UUID;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import com.trade.producer.model.TradeEvent;
import com.trade.producer.producer.TradeEventProducer;

@Component
public class TradeEventScheduler {
    
    private final TradeEventProducer producer;
    private final Random random = new Random();
    
    public TradeEventScheduler(TradeEventProducer producer) {
        this.producer = producer;
    }

    @Scheduled(fixedRate = 3000)
    public void generateTradeEvent() {
        TradeEvent event = new TradeEvent(
            "evt-" + UUID.randomUUID(),
            "trd-" + random.nextInt(5),
            randomEventType(),
            Instant.now(),
            BigDecimal.valueOf(1000 + random.nextInt(10000)),
            BigDecimal.valueOf(90 + random.nextDouble()*20).setScale(2, RoundingMode.HALF_UP),
            randomFrom(List.of("UBS", "CS", "JPM", "CITI", "BNP")),
            randomFrom(List.of("BOND-XS123", "EQUITY-IBM", "FX-EUR-CHF", "SWAP-CHF-5Y")), 
            randomFrom(List.of("CHF", "EUR", "USD"))
        );

        producer.sendTradeEvent(event);
    }

    private String randomEventType() {
        return randomFrom(List.of("NEW", "AMEND", "CANCEL"));
    }

    public String randomFrom(List<String> values) {
        return values.get(random.nextInt(values.size()));
    }
    
}
