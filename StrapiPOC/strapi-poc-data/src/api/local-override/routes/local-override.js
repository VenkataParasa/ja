'use strict';

/**
 * local-override router
 */

const { createCoreRouter } = require('@strapi/strapi').factories;

module.exports = createCoreRouter('api::local-override.local-override');
