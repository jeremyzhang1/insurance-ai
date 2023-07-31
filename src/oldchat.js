import React, { useState, useCallback } from 'react';
import axios from 'axios';
import { Box, TextField, Button, Card, CardContent, Typography, CardActions, Grid, CircularProgress } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import './Chat.css';

const Chat = () => {
  const [messages, setMessages] = useState([{ text: "Hello! How can I assist you with your insurance documents?", sender: 'AI' }]);
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
            <Card
              sx={{
                bgcolor: message.sender === 'User' ? '#e1f5fe' : '#f5f5f5',
                boxShadow: 3,
                p: 2,
                borderRadius: 8,
                ml: message.sender === 'User' ? 'auto' : '0',
                mr: message.sender === 'AI' ? 'auto' : '0',
              }}
            >
              <CardContent>
                <Typography color="text.secondary" variant="subtitle2" gutterBottom>
                  {message.sender}
                </Typography>
                <Typography variant="body1">
                  {message.text}
                </Typography>
                {message.image && <img src={`http://localhost:5000/static/${message.image}`} alt="AI response" style={{ marginTop: '10px', borderRadius: '8px' }} />}
              </CardContent>
            </Card>
          </Grid>
        ))}
        {isLoading && (
          <Grid item xs={12} sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <CircularProgress color="primary" />
            <Typography color="text.secondary" variant="subtitle2" sx={{ marginLeft: '10px' }}>
              AI is typing...
            </Typography>
          </Grid>
        )}
      </Grid>
      <form onSubmit={handleSubmit} style={{ marginTop: '20px' }}>
        <TextField
          value={input}
          onChange={handleInputChange}
          fullWidth
          variant="outlined"
          label="Type your message here..."
          size="small"
          autoFocus
        />
        <CardActions style={{ justifyContent: 'flex-end', marginTop: '10px' }}>
          <Button
            type="submit"
            color="primary"
            endIcon={<SendIcon />}
            disabled={isLoading || !input.trim()}
            variant="contained"
          >
            Send
          </Button>
        </CardActions>
      </form>
      {error && <Typography color="error" sx={{ marginTop: '10px' }}>{error}</Typography>}
    </Box>
  );
};

export default Chat;
