# Centralized prompt templates for agent nodes.
STRATEGIST_PROMPT = """
You are the Chief Strategy Officer. 
Analyze the following raw intelligence regarding: {query}

<RAW_INTEL>
{raw_data}
</RAW_INTEL>

Provide a strategic executive summary including:
1. Key Market Shift
2. Threat Level (Low/Med/High)
3. Recommended Counter-Move
"""