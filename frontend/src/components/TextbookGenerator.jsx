import React, { useState, useEffect, useCallback } from 'react';
import './TextbookGenerator.css';
import FormatCustomizer from './FormatCustomizer';
import ExportOptions from './ExportOptions'; // Import the new component

const TextbookGenerator = () => {
  const initialFormData = {
    subject_area: '',
    target_audience: 'High School',
    chapter_topics: [''],
    style_preferences: {
      include_exercises: true,
      include_summaries: true,
      include_diagrams: true
    },
    format_preferences: { // Initial format preferences
      font_size: 'medium',
      layout: 'standard'
    }
  };

  const [formData, setFormData] = useState(initialFormData);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isExporting, setIsExporting] = useState(false); // New state for export loading
  const [progress, setProgress] = useState(0);
  const [statusMessage, setStatusMessage] = useState('');
  const [generatedTextbookId, setGeneratedTextbookId] = useState(null);
  const [savedParameterSets, setSavedParameterSets] = useState([]); // New state for saved parameter sets
  const [selectedSavedSetId, setSelectedSavedSetId] = useState(''); // New state for selected saved set
  const [newParameterSetName, setNewParameterSetName] = useState(''); // New state for naming new parameter set

  // Function to fetch saved parameter sets
  const fetchSavedParameterSets = useCallback(async () => {
    try {
      const response = await fetch('/api/v1/parameters/');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setSavedParameterSets(data);
    } catch (error) {
      console.error('Error fetching saved parameter sets:', error);
      setStatusMessage(`Error fetching saved sets: ${error.message}`);
    }
  }, []);

  // Fetch saved parameter sets on component mount
  useEffect(() => {
    fetchSavedParameterSets();
  }, [fetchSavedParameterSets]);


  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;

    if (type === 'checkbox') {
      setFormData(prev => ({
        ...prev,
        style_preferences: {
          ...prev.style_preferences,
          [name]: checked
        }
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  // Handler for FormatCustomizer changes
  const handleFormatPreferencesChange = (newPreferences) => {
    setFormData(prev => ({
      ...prev,
      format_preferences: newPreferences
    }));
  };

  const handleTopicChange = (index, value) => {
    const newTopics = [...formData.chapter_topics];
    newTopics[index] = value;
    setFormData(prev => ({
      ...prev,
      chapter_topics: newTopics
    }));
  };

  const addTopicField = () => {
    setFormData(prev => ({
      ...prev,
      chapter_topics: [...prev.chapter_topics, '']
    }));
  };

  const removeTopicField = (index) => {
    if (formData.chapter_topics.length > 1) {
      const newTopics = formData.chapter_topics.filter((_, i) => i !== index);
      setFormData(prev => ({
        ...prev,
        chapter_topics: newTopics
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsGenerating(true);
    setProgress(0);
    setStatusMessage('Starting generation...');

    try {
      const response = await fetch('/api/v1/textbooks/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData), // formData now includes format_preferences
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setGeneratedTextbookId(result.textbook_id);
      setStatusMessage('Generation completed successfully!');

      // Poll for progress
      await pollForProgress(result.textbook_id);
    } catch (error) {
      console.error('Error generating textbook:', error);
      setStatusMessage(`Error: ${error.message}`);
    } finally {
      setIsGenerating(false);
    }
  };

  const pollForProgress = async (textbookId) => {
    let status = 'generating';
    while (status === 'generating') {
      try {
        await new Promise(resolve => setTimeout(resolve, 2000)); // Wait 2 seconds between polls
        const response = await fetch(`/api/v1/textbooks/generation-status/${textbookId}`);

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const statusData = await response.json();
        setProgress(statusData.progress * 100);
        setStatusMessage(statusData.message);

        status = statusData.status;

        if (status === 'completed') {
          setStatusMessage('Textbook generation completed!');
          break;
        } else if (status === 'failed') {
          setStatusMessage('Textbook generation failed.');
          break;
        }
      } catch (error) {
        console.error('Error polling for progress:', error);
        setStatusMessage(`Error checking progress: ${error.message}`);
        break;
      }
    }
  };

  const handleExport = async (textbookId, format) => {
    setIsExporting(true);
    setStatusMessage(`Exporting to ${format.toUpperCase()}...`);
    try {
      const response = await fetch(`/api/v1/textbooks/${textbookId}/export?format=${format}`, {
        method: 'POST',
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! status: ${response.status} - ${errorText}`);
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `textbook-${textbookId}.${format}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
      setStatusMessage(`Export to ${format.toUpperCase()} successful!`);
    } catch (error) {
      console.error('Error exporting textbook:', error);
      setStatusMessage(`Error exporting: ${error.message}`);
    } finally {
      setIsExporting(false);
    }
  };

  const handleSaveParameters = async () => {
    if (!newParameterSetName.trim()) {
      setStatusMessage('Please enter a name for the parameter set.');
      return;
    }
    setStatusMessage('Saving parameters...');
    try {
      const payload = {
        name: newParameterSetName,
        description: `Saved from form on ${new Date().toLocaleString()}`,
        parameters: formData, // Save the entire formData
      };
      const response = await fetch('/api/v1/parameters/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`HTTP error! status: ${response.status} - ${errorData.detail}`);
      }

      setStatusMessage(`Parameter set "${newParameterSetName}" saved successfully!`);
      setNewParameterSetName('');
      fetchSavedParameterSets(); // Refresh the list
    } catch (error) {
      console.error('Error saving parameters:', error);
      setStatusMessage(`Error saving parameters: ${error.message}`);
    }
  };

  const handleLoadParameters = async () => {
    if (!selectedSavedSetId) {
      setStatusMessage('Please select a parameter set to load.');
      return;
    }
    setStatusMessage('Loading parameters...');
    try {
      const response = await fetch(`/api/v1/parameters/${selectedSavedSetId}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      // Ensure chapter_topics is an array of strings, add empty if needed
      const loadedParameters = {
          ...data.parameters,
          chapter_topics: data.parameters.chapter_topics.length > 0
            ? data.parameters.chapter_topics
            : ['']
      };
      setFormData(loadedParameters);
      setStatusMessage(`Parameter set "${data.name}" loaded successfully!`);
    } catch (error) {
      console.error('Error loading parameters:', error);
      setStatusMessage(`Error loading parameters: ${error.message}`);
    }
  };

  return (
    <div className="textbook-generator">
      <h2>Generate Custom Textbook</h2>

      <div className="parameter-management-section">
        <h3>Saved Parameter Sets</h3>
        <div className="form-group">
          <label htmlFor="save-param-name">Save Current Parameters As:</label>
          <input
            type="text"
            id="save-param-name"
            value={newParameterSetName}
            onChange={(e) => setNewParameterSetName(e.target.value)}
            placeholder="Enter name for saved set"
            disabled={isGenerating || isExporting}
          />
          <button
            type="button"
            onClick={handleSaveParameters}
            disabled={isGenerating || isExporting || !newParameterSetName.trim()}
          >
            Save Parameters
          </button>
        </div>

        <div className="form-group">
          <label htmlFor="load-param-select">Load Saved Parameters:</label>
          <select
            id="load-param-select"
            value={selectedSavedSetId}
            onChange={(e) => setSelectedSavedSetId(e.target.value)}
            disabled={isGenerating || isExporting || savedParameterSets.length === 0}
          >
            <option value="">-- Select a set --</option>
            {savedParameterSets.map(set => (
              <option key={set.id} value={set.id}>{set.name} ({new Date(set.created_at).toLocaleDateString()})</option>
            ))}
          </select>
          <button
            type="button"
            onClick={handleLoadParameters}
            disabled={isGenerating || isExporting || !selectedSavedSetId}
          >
            Load Selected
          </button>
          <button
            type="button"
            onClick={fetchSavedParameterSets}
            disabled={isGenerating || isExporting}
            className="refresh-btn"
          >
            Refresh List
          </button>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="generator-form">
        <div className="form-group">
          <label htmlFor="subject_area">Subject Area:</label>
          <input
            type="text"
            id="subject_area"
            name="subject_area"
            value={formData.subject_area}
            onChange={handleInputChange}
            required
            disabled={isGenerating}
          />
        </div>

        <div className="form-group">
          <label htmlFor="target_audience">Target Audience:</label>
          <select
            id="target_audience"
            name="target_audience"
            value={formData.target_audience}
            onChange={handleInputChange}
            disabled={isGenerating}
          >
            <option value="Elementary School">Elementary School</option>
            <option value="Middle School">Middle School</option>
            <option value="High School">High School</option>
            <option value="University">University</option>
            <option value="Professional">Professional</option>
          </select>
        </div>

        <div className="form-group">
          <label>Chapter Topics:</label>
          {formData.chapter_topics.map((topic, index) => (
            <div key={index} className="topic-input-group">
              <input
                type="text"
                value={topic}
                onChange={(e) => handleTopicChange(index, e.target.value)}
                placeholder={`Chapter ${index + 1} topic`}
                required
                disabled={isGenerating}
              />
              {formData.chapter_topics.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeTopicField(index)}
                  disabled={isGenerating}
                  className="remove-topic-btn"
                >
                  Remove
                </button>
              )}
            </div>
          ))}
          <button
            type="button"
            onClick={addTopicField}
            disabled={isGenerating}
            className="add-topic-btn"
          >
            Add Chapter Topic
          </button>
        </div>

        <div className="form-group">
          <label>Style Preferences:</label>
          <div className="checkbox-group">
            <label>
              <input
                type="checkbox"
                name="include_exercises"
                checked={formData.style_preferences.include_exercises}
                onChange={handleInputChange}
                disabled={isGenerating}
              />
              Include Exercises
            </label>
            <label>
              <input
                type="checkbox"
                name="include_summaries"
                checked={formData.style_preferences.include_summaries}
                onChange={handleInputChange}
                disabled={isGenerating}
              />
              Include Summaries
            </label>
            <label>
              <input
                type="checkbox"
                name="include_diagrams"
                checked={formData.style_preferences.include_diagrams}
                onChange={handleInputChange}
                disabled={isGenerating}
              />
              Include Diagrams
            </label>
          </div>
        </div>

        {/* Integrate FormatCustomizer component */}
        <FormatCustomizer
          initialPreferences={formData.format_preferences}
          onPreferencesChange={handleFormatPreferencesChange}
        />

        <button
          type="submit"
          disabled={isGenerating || !formData.subject_area || formData.chapter_topics.some(topic => !topic.trim())}
          className="generate-btn"
        >
          {isGenerating ? 'Generating...' : 'Generate Textbook'}
        </button>
      </form>

      {(isGenerating || isExporting) && ( // Update conditional display for progress/status
        <div className="progress-section">
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <p className="status-message">{statusMessage}</p>
        </div>
      )}

      {generatedTextbookId && !isGenerating && (
        <div className="result-section">
          <p>Textbook generated successfully!</p>
          <p>Textbook ID: {generatedTextbookId}</p>
          {/* Integrate ExportOptions component */}
          <ExportOptions
            textbookId={generatedTextbookId}
            onExport={handleExport}
            disabled={isExporting}
          />
        </div>
      )}
    </div>
  );
};

export default TextbookGenerator;