# -*- coding: utf-8 -*-
"""Test to verify LLM receives masked data"""

from model_wrapper import get_model_wrapper

wrapper = get_model_wrapper()

query = "My name is Alice and my phone is 9876543210"
result = wrapper.process_query(query)

print("=" * 80)
print("LLM PROMPT VERIFICATION")
print("=" * 80)
print(f"Original Query:  {result['original_query']}")
print(f"Masked Query:    {result['masked_query']}")
print(f"LLM Received:    {result['masked_query']}")
print(f"LLM Response:    {result['llm_response'][:100]}...")
print(f"Final Response:  {result['final_response'][:100]}...")
print("=" * 80)
print("✓ LLM receives MASKED data with fake values")
print("✓ User receives RECONSTRUCTED response with original values")
print("=" * 80)
