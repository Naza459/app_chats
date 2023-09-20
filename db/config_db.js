const mysql = require('mysql');

const dbConnection = () => {
  const connection = mysql.createConnection({
    host: process.env.DATABASE_HOST,
    user: process.env.DATABASE_USER,
    password: process.env.DATABASE_PASSWORD,
    database: process.env.DATABASE_NAME,
  });

  connection.connect((error) => {
    if (error) {
      console.error('Error al conectar a la base de datos:', error);
      throw new Error('Error al conectar a la base de datos');
    }
    console.log('Conexión a la base de datos establecida!');
  });

  return connection;
};

module.exports = {
  dbConnection,
};