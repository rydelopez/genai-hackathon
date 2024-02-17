'use client';

import React, { useState, useRef } from 'react';

import { Button } from '@nextui-org/react';
import { MicrophoneIcon, StopIcon } from '@heroicons/react/24/solid';

function AudioRecorderButton() {
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const [audioData, setAudioData] = useState(null);

  const startRecording = async () => {
    if (isRecording) return;

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      mediaRecorderRef.current.ondataavailable = handleDataAvailable;
      mediaRecorderRef.current.start();

      setIsRecording(true);
    } catch (err) {
      console.error('Error accessing audio device:', err);
    }
  };

  const stopRecording = () => {
    if (!isRecording) return;

    mediaRecorderRef.current.stop();
    setIsRecording(false);
  };

  const handleDataAvailable = (event) => {
    if (event.data.size > 0) {
      setAudioData(event.data);
    }
  };

  const sendAudioToServer = async () => {
    if (!audioData) return;

    const formData = new FormData();
    formData.append('audio', audioData, 'student_recording.webm');
    formData.append('');

    try {
      const response = await fetch('http://localhost:3500/student/chat', {
        method: 'POST',
        body: formData,
      });
      console.log('Sending audio to backend...');
      const result = await response.json();
      console.log(result);
    } catch (err) {
      console.error('Failed to send audio:', err);
    }
  };

  const toggleRecording = () => {
    if (isRecording) {
      stopRecording();
      sendAudioToServer();
    } else {
      startRecording();
    }
  };

  return (
    <Button
      className="h-36 w-36 rounded-full bg-gradient-to-tr from-pink-500 to-yellow-500 text-white shadow-lg"
      onClick={toggleRecording}
    >
      {isRecording ? (
        <StopIcon className="text-white-500 h-96 w-96" />
      ) : (
        <MicrophoneIcon className="text-white-500 h-96 w-96" />
      )}
    </Button>
  );
}

export default function Student() {
  return (
    <main className="mx-auto max-w-7xl p-4 md:p-10">
      <div className="flex justify-center">
        <AudioRecorderButton />
      </div>
    </main>
  );
}
