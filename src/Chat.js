import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { Box, TextField, Button, Card, CardContent, Typography, CardActions, Grid, CircularProgress } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getNextMessage = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get('http://localhost:5000/next');
      addAIMessageToChat(response);
    } catch (error) {
      setError('Error communicating with server. Please try again later.');
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    getNextMessage();
  }, [getNextMessage]);

  const handleInputChange = (event) => {
    setInput(event.target.value);
  };

  const addAIMessageToChat = (response) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      {
        text: response.data.text,
        image: response.data.image_path,
        sender: 'AI'
      },
    ]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    setMessages([...messages, { text: input, sender: 'User' }]);

    try {
      if (input.trim().endsWith('?')) {
        const response = await axios.post('http://localhost:5000/search', { search_term: input });
        addAIMessageToChat(response);
      } else {
        getNextMessage();
      }
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
                bgcolor: message.sender === 'User' ? 'lightblue' : 'lightgrey',
                boxShadow: 3,
                p: 1,
                borderRadius: 2,
                ml: message.sender === 'User' ? 'auto' : '0',
                mr: message.sender === 'AI' ? 'auto' : '0',
              }}
            >
              <CardContent>
                <Typography color="text.secondary" gutterBottom>
                  {message.sender}
                </Typography>
                <Typography variant="body2">
                  {message.text}
                </Typography>
                {message.image && <img src={`http://localhost:5000/static/${message.image}`} alt="AI response" />}
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
        />
        <CardActions>
          <Button
            type="submit"
            color="primary"
            endIcon={<SendIcon />}
            disabled={isLoading}
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
