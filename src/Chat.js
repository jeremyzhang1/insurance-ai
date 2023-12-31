import React, { useState, useCallback } from 'react';
import axios from 'axios';
import { Box, TextField, Button, Card, CardContent, Typography, CardActions, Grid, CircularProgress } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import './Chat.css';

const Chat = () => {
  const [messages, setMessages] = useState([{ text: "Hello! How can I assist you with your insurance plan summary of benefits and coverage statement with insurance company 1?", sender: 'AI' }]);
  const [input, setInput] = useState('');
  const [isLoading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = useCallback((event) => {
    setInput(event.target.value);
  }, []);

  const addMessageToChat = useCallback((text, sender) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      { text, sender },
    ]);
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    addMessageToChat(input, 'User');

    try {
      const response = await axios.post('http://localhost:5000/next', { prompt: input });
      addMessageToChat(response.data.answer, 'AI');
    } catch (error) {
      setError('Error communicating with server. Please try again later.');
    }
    setInput('');
    setLoading(false);
  };

  return (
    <Box sx={{ p: 3, maxHeight: '80vh', overflow: 'auto' }}>
      <Grid container spacing={2}>
        {messages.map((message, index) => (
          <Grid item xs={12} key={index}>
            <Card className={`message-card ${message.sender.toLowerCase()}`}>
    <CardContent className="message-card-content">
        <Typography color={message.sender === 'User' ? "text.primary" : "text.secondary"} gutterBottom>
            {message.sender}
        </Typography>
        <Typography variant="body2" style={{ color: message.sender === 'User' ? 'white' : 'black' }}>
            {message.text}
        </Typography>
        {message.image && 
            <img src={`http://localhost:5000/static/${message.image}`} alt="AI response" />}
    </CardContent>
</Card>

          </Grid>
        ))}
        {isLoading && (
          <Grid item xs={12}>
            <Typography color="text.secondary" gutterBottom>
              AI is typing...
            </Typography>
            <CircularProgress />
          </Grid>
        )}
      </Grid>
      <form onSubmit={handleSubmit}>
        <TextField
          value={input}
          onChange={handleInputChange}
          fullWidth
          margin="normal"
          label="Type your message here..."
          variant="outlined"
          size="small"
          autoFocus 
        />
        <CardActions>
          <Button
            type="submit"
            color="primary"
            endIcon={<SendIcon />}
            disabled={isLoading || !input.trim()} 
          >
            Send
          </Button>
        </CardActions>
      </form>
      {error && <Typography color="error">{error}</Typography>}
    </Box>
  );
};

export default Chat;
