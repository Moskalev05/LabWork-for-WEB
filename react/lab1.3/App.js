import React from 'react';

const StockTable = () => {
  const stocks = [
    {
      stock_name: "EFX",
      company_name: "Equifax Inc",
      price: 163.55,
      currency: "USD",
      change: "+9.03"
    }, {
      stock_name: "IRM",
      company_name: "Iron Mountain Inc",
      price: 33.21,
      currency: "USD",
      change: "+1.42"
    }, {
      stock_name: "NTAP",
      company_name: "NetApp Inc",
      price: 54.81,
      currency: "USD",
      change: "-6.01"
    }, {
      stock_name: "CTL",
      company_name: "Centurylink Inc",
      price: 13.79,
      currency: "USD",
      change: "-1.37"
    }
  ];

  return (
    <div style={{ margin: '20px' }}>
      <h2>Stock Prices</h2>
      <table style={{ borderCollapse: 'collapse', width: '100%', maxWidth: '800px' }}>
        <thead>
          <tr style={{ backgroundColor: '#f2f2f2' }}>
            <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>Symbol</th>
            <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>Company</th>
            <th style={{ padding: '12px', textAlign: 'right', borderBottom: '1px solid #ddd' }}>Price</th>
            <th style={{ padding: '12px', textAlign: 'right', borderBottom: '1px solid #ddd' }}>Change</th>
          </tr>
        </thead>
        <tbody>
          {stocks.map((stock, index) => (
            <tr key={index} style={{ borderBottom: '1px solid #ddd' }}>
              <td style={{ padding: '12px', textAlign: 'left' }}>{stock.stock_name}</td>
              <td style={{ padding: '12px', textAlign: 'left' }}>{stock.company_name}</td>
              <td style={{ padding: '12px', textAlign: 'right' }}>{stock.price.toFixed(2)} {stock.currency}</td>
              <td style={{ 
                padding: '12px', 
                textAlign: 'right', 
                color: stock.change.startsWith('+') ? 'green' : 'red',
                fontWeight: 'bold'
              }}>
                {stock.change}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StockTable;