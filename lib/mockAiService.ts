/**
 * Mock AI Service for simulating AI responses
 */

export async function getMockReply(message: string): Promise<string> {
  // Simulate network delay of 1.5 seconds
  await new Promise(resolve => setTimeout(resolve, 1500));

  const lowerMessage = message.toLowerCase();

  // Keyword logic for different responses
  if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
    return "Hello! How can I help you manage your tasks today?";
  } else if (lowerMessage.includes('add')) {
    return "I have added that task for you! (Mock)";
  } else if (lowerMessage.includes('list') || lowerMessage.includes('show')) {
    return "Here are your pending tasks... (Mock)";
  } else {
    return "I received your message. Since I am a mock AI, I can't do much yet!";
  }
}