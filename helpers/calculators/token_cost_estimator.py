import logging

log = logging.getLogger(__name__)

def distribute_tokens(tokens_per_output, total_completion_tokens):
    current_total = sum(tokens_per_output)
    if total_completion_tokens > current_total:
        remaining_tokens = total_completion_tokens - current_total
        num_outputs = len(tokens_per_output)

        log.debug(f"Distributing {remaining_tokens} tokens for {num_outputs} outputs.")
        for i in range(remaining_tokens):
            tokens_per_output[i % num_outputs] += 1

    log.debug(f"Adjusted tokens per output: {tokens_per_output}")
    return tokens_per_output

def increment_tokens(tokens_tracker, index, token_increment):
    tokens_tracker[index] += token_increment
    log.debug(f"Incremented token count for output {index} by {token_increment}. Current count: {tokens_tracker[index]}")

def calculate_individual_cost(tokens_used):
    cost_per_token = 0.00002
    estimated_cost = [tokens * cost_per_token for tokens in tokens_used]

    for idx, cost in enumerate(estimated_cost):
        log.info(f"Estimated cost for output {idx + 1}: ${cost:.6f} for {tokens_used[idx]} tokens.")
    
    return estimated_cost

def calculate_total_cost(tokens_used, estimated_cost):
    total_tokens = sum(tokens_used)
    total_cost = sum(estimated_cost)
    log.info(f"Total tokens used: {total_tokens}")
    log.info(f"Total estimated cost: ${total_cost:.6f}")
    return total_tokens, total_cost
