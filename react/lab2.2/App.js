import React, { useState } from 'react';

const ProfessionSelector = ({ onProfessionChange }) => {
  const professions = [
    { id: 'developer', name: 'Разработчик' },
    { id: 'designer', name: 'Дизайнер' },
    { id: 'manager', name: 'Менеджер' },
    { id: 'marketer', name: 'Маркетолог' },
    { id: 'analyst', name: 'Аналитик' }
  ];

  const [selectedProfession, setSelectedProfession] = useState('developer');

  const handleChange = (e) => {
    const value = e.target.value;
    setSelectedProfession(value);
    onProfessionChange(value);
  };

  return (
    <div style={{
      marginBottom: '30px',
      padding: '20px',
      backgroundColor: '#f5f5f5',
      borderRadius: '8px'
    }}>
      <h2 style={{ marginTop: 0, color: '#333' }}>Выберите профессию:</h2>
      <div style={{ 
        display: 'flex', 
        flexWrap: 'wrap', 
        gap: '15px' 
      }}>
        {professions.map(profession => (
          <label
            key={profession.id}
            style={{
              display: 'flex',
              alignItems: 'center',
              padding: '10px 15px',
              backgroundColor: selectedProfession === profession.id ? '#e9e9e9' : 'white',
              borderRadius: '4px',
              cursor: 'pointer',
              transition: 'background-color 0.2s'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = '#e9e9e9';
            }}
            onMouseLeave={(e) => {
              if (selectedProfession !== profession.id) {
                e.currentTarget.style.backgroundColor = 'white';
              }
            }}
          >
            <input
              type="radio"
              name="profession"
              value={profession.id}
              checked={selectedProfession === profession.id}
              onChange={handleChange}
              style={{ marginRight: '8px' }}
            />
            {profession.name}
          </label>
        ))}
      </div>
    </div>
  );
};

const JobMenu = ({ profession }) => {
  const menuItems = { developer: [
      { title: 'GitHub', url: 'https://github.com' },
      { title: 'Stack Overflow', url: 'https://stackoverflow.com' },
      { title: 'MDN Web Docs', url: 'https://developer.mozilla.org' },
      { title: 'Dev.to', url: 'https://dev.to' },
      { title: 'Codewars', url: 'https://codewars.com' },
      { title: 'LeetCode', url: 'https://leetcode.com' },
      { title: 'HackerRank', url: 'https://hackerrank.com' }
    ],
    designer: [
      { title: 'Dribbble', url: 'https://dribbble.com' },
      { title: 'Behance', url: 'https://behance.net' },
      { title: 'Figma', url: 'https://figma.com' },
      { title: 'Adobe Creative Cloud', url: 'https://adobe.com/creativecloud' },
      { title: 'Awwwards', url: 'https://awwwards.com' },
      { title: 'UI Movement', url: 'https://uimovement.com' },
      { title: 'Color Hunt', url: 'https://colorhunt.co' }
    ],
    manager: [
      { title: 'Trello', url: 'https://trello.com' },
      { title: 'Asana', url: 'https://asana.com' },
      { title: 'Jira', url: 'https://atlassian.com/software/jira' },
      { title: 'Notion', url: 'https://notion.so' },
      { title: 'Slack', url: 'https://slack.com' },
      { title: 'Harvard Business Review', url: 'https://hbr.org' },
      { title: 'MindTools', url: 'https://mindtools.com' }
    ],
    marketer: [
      { title: 'Google Analytics', url: 'https://analytics.google.com' },
      { title: 'HubSpot', url: 'https://hubspot.com' },
      { title: 'Mailchimp', url: 'https://mailchimp.com' },
      { title: 'SEMrush', url: 'https://semrush.com' },
      { title: 'Ahrefs', url: 'https://ahrefs.com' },
      { title: 'Buffer', url: 'https://buffer.com' },
      { title: 'Social Media Examiner', url: 'https://socialmediaexaminer.com' }
    ],
    analyst: [
      { title: 'Tableau', url: 'https://tableau.com' },
      { title: 'Power BI', url: 'https://powerbi.microsoft.com' },
      { title: 'Google Data Studio', url: 'https://datastudio.google.com' },
      { title: 'Kaggle', url: 'https://kaggle.com' },
      { title: 'Towards Data Science', url: 'https://towardsdatascience.com' },
      { title: 'Statista', url: 'https://statista.com' },
      { title: 'FiveThirtyEight', url: 'https://fivethirtyeight.com' }
    ] };

  return (
    <div style={{
      padding: '20px',
      backgroundColor: '#f9f9f9',
      borderRadius: '8px'
    }}>
      <h3 style={{ marginTop: 0, color: '#444' }}>
        Полезные ресурсы для {getProfessionName(profession)}:
      </h3>
      <ul style={{ listStyleType: 'none', padding: 0 }}>
        {menuItems[profession].map((item, index) => (
          <li key={index} style={{ marginBottom: '10px' }}>
            <a
              href={item.url}
              target="_blank"
              rel="noopener noreferrer"
              style={{
                display: 'block',
                padding: '8px 12px',
                color: '#0066cc',
                textDecoration: 'none',
                borderRadius: '4px',
                transition: 'background-color 0.2s'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = '#e6f2ff';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'transparent';
              }}
            >
              {item.title}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

// Вспомогательная функция остается без изменений
const getProfessionName = (id) => { const names = {
    developer: 'разработчиков',
    designer: 'дизайнеров',
    manager: 'менеджеров',
    marketer: 'маркетологов',
    analyst: 'аналитиков'
  };
  return names[id] || ''; };

const JobMenuApp = () => {
  const [currentProfession, setCurrentProfession] = useState('developer');

  return (
    <div style={{
      maxWidth: '800px',
      margin: '0 auto',
      padding: '20px',
      fontFamily: 'Arial, sans-serif'
    }}>
      <h1>Профессиональные ресурсы</h1>
      <ProfessionSelector onProfessionChange={setCurrentProfession} />
      <JobMenu profession={currentProfession} />
    </div>
  );
};

export default JobMenuApp;