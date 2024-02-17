// components/FileList.js
import React from 'react';

const FileList = ({ files, onDelete }) => {
  return (
    <div style={{ height: '300px', overflowY: 'scroll', border: '1px solid #ccc', padding: '10px' }}>
      {files != undefined && files.map((file, index) => (
        <div key={index} style={{ marginBottom: '10px' }}>
          <span>{file.name}</span>
          <button onClick={() => onDelete(file.name)} style={{ marginLeft: '10px' }}>X</button>
        </div>
      ))}
    </div>
  );
};

export default FileList;
