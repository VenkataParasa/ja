'use strict';

/**
 * local-override service
 */

const { createCoreService } = require('@strapi/strapi').factories;

module.exports = createCoreService('api::local-override.local-override');
