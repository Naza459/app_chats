const Sequelize = require('sequelize');

// Crea una instancia de Sequelize con la configuración de tu base de datos
const sequelize = new Sequelize({
  dialect: 'mysql',
  host: process.env.DATABASE_HOST,
  username: process.env.DATABASE_USER,
  password: process.env.DATABASE_PASSWORD,
  database: process.env.DATABASE_NAME,
});

// Define el modelo para tu tabla
const Usuario = sequelize.define('Usuario', {
  id: {
    type: Sequelize.INTEGER,
    autoIncrement: true,
    primaryKey: true,
  },
  name: {
    type: Sequelize.STRING,
    allowNull: false,
  },
  username: {
    type: Sequelize.STRING,
    allowNull: false,
  },
  password: {
    type: Sequelize.STRING,
    allowNull: false,
  },
  email: {
    type: Sequelize.STRING,
    allowNull: false,
    unique: true,
  },
  rol: {
    type: Sequelize.STRING,
    allowNull: false,
  },
  created: {
    type: Sequelize.DATE,
    defaultValue: Sequelize.NOW,
  },
  modified: {
    type: Sequelize.DATE,
    defaultValue: Sequelize.NOW,
  },
});

// Hook para actualizar el campo "modified" antes de cada actualización
Usuario.beforeUpdate((usuario) => {
  usuario.modified = new Date();
});

// Define el modelo para tu tabla
const Cliente = sequelize.define('Cliente', {
  id: {
    type: Sequelize.INTEGER,
    autoIncrement: true,
    primaryKey: true,
  },
  name: {
    type: Sequelize.STRING,
    allowNull: false,
  },
  username: {
    type: Sequelize.STRING,
    allowNull: false,
  },
  password: {
    type: Sequelize.STRING,
    allowNull: false,
  },
  email: {
    type: Sequelize.STRING,
    allowNull: false,
    unique: true,
  },
  rol: {
    type: Sequelize.STRING,
    allowNull: false,
  },
  created: {
    type: Sequelize.DATE,
    defaultValue: Sequelize.NOW,
  },
  modified: {
    type: Sequelize.DATE,
    defaultValue: Sequelize.NOW,
  },
});

// Hook para actualizar el campo "modified" antes de cada actualización
Cliente.beforeUpdate((Cliente) => {
  Cliente.modified = new Date();
});

// Define el modelo para tu tabla
const Conversacion  = sequelize.define('Conversacion', {
  id: {
    type: Sequelize.INTEGER,
    autoIncrement: true,
    primaryKey: true,
  },
  type_messages: {
    type: Sequelize.STRING,
    allowNull: false,
  },
  messages: {
    type: Sequelize.STRING,
    allowNull: false,
  },
  file: {
    type: Sequelize.STRING,
    allowNull: true,
  },
  
  created: {
    type: Sequelize.DATE,
    defaultValue: Sequelize.NOW,
  },
  modified: {
    type: Sequelize.DATE,
    defaultValue: Sequelize.NOW,
  },
});

// Establece la relación entre Usuario y Conversacion
Usuario.hasMany(Conversacion, { foreignKey: 'usuarioId' });
Conversacion.belongsTo(Usuario, { foreignKey: 'usuarioId' })
Cliente.hasMany(Conversacion, { foreignKey: 'clienteId' });
Conversacion.belongsTo(Cliente, { foreignKey: 'clienteId' })

// Hook para actualizar el campo "modified" antes de cada actualización
Conversacion.beforeUpdate((Conversacion) => {
  Conversacion.modified = new Date();
});


// Define el modelo para tu tabla
const Catalogo  = sequelize.define('Catalogo', {
  id: {
    type: Sequelize.INTEGER,
    autoIncrement: true,
    primaryKey: true,
  },
  type_product: {
    type: Sequelize.STRING,
    allowNull: false,
  },
  name_product: {
    type: Sequelize.STRING,
    allowNull: false,
  },
  precio: {
    type: Sequelize.FLOAT,
    allowNull: true,
  },
  is_enabled: {
    type: Sequelize.BOOLEAN,
    defaultValue: true,
    allowNull: true,
  },
  
  created: {
    type: Sequelize.DATE,
    defaultValue: Sequelize.NOW,
  },
  modified: {
    type: Sequelize.DATE,
    defaultValue: Sequelize.NOW,
  },
});

// Hook para actualizar el campo "modified" antes de cada actualización
Catalogo.beforeUpdate((Catalogo) => {
  Catalogo.modified = new Date();
});

// Sincroniza el modelo con la base de datos (crea la tabla si no existe)
sequelize.sync()
  .then(() => console.log('Modelos sincronizados con la base de datos'))
  .catch((error) => console.error('Error al sincronizar modelos:', error));

// Exporta el modelo para que pueda ser utilizado en otros archivos
module.exports = {
  Usuario,
  Cliente,
  Conversacion,
  Catalogo
};