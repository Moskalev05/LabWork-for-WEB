import React from 'react';
import PropTypes from 'prop-types';

class Clock extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      time: new Date()
    };
    
    // Стили
    this.styles = {
      container: {
        display: 'inline-flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: '20px',
        backgroundColor: '#f5f5f5',
        borderRadius: '10px',
        boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
        fontFamily: '"Arial", sans-serif',
        margin: '10px'
      },
      clockFace: {
        fontSize: '2rem',
        fontWeight: 'bold',
        color: '#333',
        marginBottom: '10px'
      },
      clockInfo: {
        fontSize: '0.9rem',
        color: '#666'
      }
    };
  }

  componentDidMount() {
    this.timerID = setInterval(
      () => this.tick(),
      1000
    );
  }

  componentWillUnmount() {
    clearInterval(this.timerID);
  }

  tick() {
    this.setState({
      time: new Date()
    });
  }

  getTimezoneOffset(timezone) {
    if (!timezone) return 0;
    
    const [_, sign, hours, minutes] = timezone.match(/([+-]?)(\d+):(\d+)/);
    const totalMinutes = (parseInt(hours) * 60 + parseInt(minutes)) * (sign === '-' ? -1 : 1);
    return totalMinutes;
  }

  formatTime() {
    const { format, timezone } = this.props;
    const { time } = this.state;

    const offsetMinutes = this.getTimezoneOffset(timezone);
    const adjustedTime = new Date(time.getTime() + offsetMinutes * 60000);

    let hours = adjustedTime.getUTCHours();
    const minutes = adjustedTime.getUTCMinutes().toString().padStart(2, '0');
    const seconds = adjustedTime.getUTCSeconds().toString().padStart(2, '0');

    let period = '';
    if (format === '12') {
      period = hours >= 12 ? ' PM' : ' AM';
      hours = hours % 12 || 12;
    }

    return `${hours.toString().padStart(2, '0')}:${minutes}:${seconds}${period}`;
  }

  render() {
    return (
      <div style={this.styles.container}>
        <div style={this.styles.clockFace}>
          {this.formatTime()}
        </div>
        <div style={this.styles.clockInfo}>
          Format: {this.props.format}-hour | Timezone: {this.props.timezone || 'local'}
        </div>
      </div>
    );
  }
}

Clock.propTypes = {
  format: PropTypes.oneOf(['12', '24']),
  timezone: PropTypes.string
};

Clock.defaultProps = {
  format: '24',
  timezone: ''
};

// Пример использования
export function App() {
  const appStyle = {
    textAlign: 'center',
    padding: '20px',
    fontFamily: '"Arial", sans-serif'
  };

  const gridStyle = {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '20px',
    marginTop: '30px'
  };

  return (
    <div style={appStyle}>
      <h1 style={{ color: '#333' }}>World Clocks</h1>
      
      <div style={gridStyle}>
        <Clock format="24" timezone="+3:00" />
        <Clock format="12" timezone="-4:00" />
        <Clock format="12" timezone="+9:00" />
        <Clock format="24" timezone="+0:00" />
        <Clock format="12" />
      </div>
    </div>
  );
}

export default Clock;