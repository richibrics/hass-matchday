from . import CONF_DATA_TYPE,CONF_DATA_ID,DOMAIN,CONF_DATA,CONF_SESSION
from homeassistant.helpers.entity import Entity
from .objects import *

async def async_setup_platform(hass, config, async_add_entities, discovery_info):
    # In discovery info I have the client ID
    """Set up the sensors."""
    client_index = discovery_info
    id = hass.data[DOMAIN][CONF_DATA][client_index][CONF_DATA_ID]
    idType = hass.data[DOMAIN][CONF_DATA][client_index][CONF_DATA_TYPE]
    session = hass.data[DOMAIN][CONF_SESSION]
    async_add_entities([MatchdaySensor(hass, config,id,idType,session)])

class MatchdaySensor(Entity):
    
    def __init__(self,hass,config, id, idType,session):
        """Initialize the sensor."""
        self.idType=idType
        self.id=id['id']
        print(self.id)
        self.session=session
        if(idType==TYPE_TEAM):
            self.object = Team(self.id,self.session)
        else:
            self.object=Tournament(self.id,self.session)
        self._name = ("Matchday_" + self.object.name).lower().replace(" ","_")
        self._state = str(len(self.object.events)) + " matches"
        self.info=self.object.ReturnData()

    @property
    def name(self):
        """Return the name of the sensor, if any."""
        return self._name


    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return the state of the sensor."""
        return {
            "name": self.object.name,
            "fixtures": self.info
        }

    async def async_update(self):
        """Retrieve latest state."""
        self.object.Update()
        self.info=self.object.ReturnData()

    @property
    def icon(self):
        """Return the icon for the sensor."""
        return "mdi:soccer"
