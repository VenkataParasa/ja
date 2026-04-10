'use strict';

/**
 * national-simulation service
 */

const { createCoreService } = require('@strapi/strapi').factories;

module.exports = createCoreService('api::national-simulation.national-simulation');
