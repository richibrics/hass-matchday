
from requests import Session


import logging


from .consts import *

import voluptuous as vol

import homeassistant.loader as loader
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
import homeassistant.util.dt as dt_util
import homeassistant.helpers.config_validation as cv
from homeassistant.components import recorder
from homeassistant.helpers.entity import Entity
from homeassistant.core import callback
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers.dispatcher import dispatcher_send
from homeassistant.helpers.event import async_track_time_interval


# The domain of your component. Should be equal to the name of your component.
DOMAIN = "matchday"

# To pass data to sensors in a dict
CONF_SESSION = "session" 
CONF_DATA = "data" 
CONF_DATA_TYPE = "type" 
CONF_DATA_ID = "id" 


# YAML setting
TEAMS_CONF_LIST_KEY = 'teams'
TOURNAMENTS_CONF_LIST_KEY = 'tournaments'
ITEM_LIST_KEY = 'id'
ALTERNATIVE_NAME_LIST_KEY = "alternative_name"

DATA_SCHEMA = vol.Schema( # Valid both for teams and tournaments
    {
        vol.Required(ITEM_LIST_KEY): cv.string,
        vol.Optional(ALTERNATIVE_NAME_LIST_KEY): cv.boolean,
    }, extra=vol.ALLOW_EXTRA
)


CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.All(
            vol.Schema(
                {
                    vol.Optional(TEAMS_CONF_LIST_KEY): vol.All(
                        cv.ensure_list, [DATA_SCHEMA]
                    ),
                    vol.Optional(TOURNAMENTS_CONF_LIST_KEY): vol.All(
                        cv.ensure_list, [DATA_SCHEMA]
                    ),
                }
            )
        )
    },
    extra=vol.ALLOW_EXTRA,
)



async def async_setup(hass, config):
    hass.data[DOMAIN]={}
    hass.data[DOMAIN][CONF_DATA]=[]
    hass.data[DOMAIN][CONF_SESSION]=Session()
    index=0
    if TEAMS_CONF_LIST_KEY in config[DOMAIN]:
        # index is the number of client info to find them in the hass.data list
        for teamId in config[DOMAIN][TEAMS_CONF_LIST_KEY]:
            # Each sensor at its own index will found the correct id and type
            hass.data[DOMAIN][CONF_DATA].append({CONF_DATA_TYPE: TYPE_TEAM,CONF_DATA_ID: teamId})
            print(teamId,TYPE_TEAM)
            # Load the sensors 
            hass.async_create_task(
                async_load_platform(
                    hass, SENSOR_DOMAIN, DOMAIN, index,  config
                )
            )
            index+=1

    if TOURNAMENTS_CONF_LIST_KEY in config[DOMAIN]:
        for tournamentId in config[DOMAIN][TOURNAMENTS_CONF_LIST_KEY]:
            print(tournamentId,TYPE_TOURNAMENT)
            # Each sensor at its own index will found the correct id and type
            hass.data[DOMAIN][CONF_DATA].append({CONF_DATA_TYPE: TYPE_TOURNAMENT,CONF_DATA_ID: tournamentId})

            # Load the sensors 
            hass.async_create_task(
                async_load_platform(
                    hass, SENSOR_DOMAIN, DOMAIN, index,  config
                )
            )
            index+=1


    def update(call=None):
        """Should update here"""
        pass

    return True
