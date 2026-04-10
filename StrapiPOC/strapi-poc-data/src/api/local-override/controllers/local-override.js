'use strict';

/**
 * local-override controller
 */

const { createCoreController } = require('@strapi/strapi').factories;

module.exports = createCoreController('api::local-override.local-override');
