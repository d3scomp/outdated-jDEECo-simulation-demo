package cz.cuni.mff.d3s.jdeeco.simulation.demo;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import cz.cuni.mff.d3s.deeco.DeecoProperties;
import cz.cuni.mff.d3s.deeco.knowledge.ReadOnlyKnowledgeManager;
import cz.cuni.mff.d3s.deeco.logging.Log;
import cz.cuni.mff.d3s.deeco.network.DirectRecipientSelector;
import cz.cuni.mff.d3s.deeco.network.KnowledgeData;

class AreaBasedSelector implements DirectRecipientSelector {

	public static final String IP_BOUNDARY_ALWAYS_ON = "demo.boundary.alwayson";

	private AreaNetworkRegistry networkRegistry = null;
	private boolean returnAll = false;
	
	public void initialize(AreaNetworkRegistry networkRegistry) {
		this.networkRegistry = networkRegistry;		
		boolean alwaysOn = Boolean.getBoolean(IP_BOUNDARY_ALWAYS_ON);
		returnAll = !alwaysOn && Boolean.getBoolean(DeecoProperties.DISABLE_BOUNDARY_CONDITIONS);
	}
	
	@Override
	public Collection<String> getRecipients(KnowledgeData data,
			ReadOnlyKnowledgeManager sender) {
		
		String ownerTeam = (String) data.getKnowledge().getValue(KnowledgePathBuilder.buildSimplePath("teamId"));

		List<String> recipients = getRecipientsForTeam(ownerTeam);
			
		Log.d(String.format("Possible direct recipients for %s(team=%s) at %s are [%s]",
				data.getMetaData().componentId, ownerTeam, sender.getId(), Arrays.deepToString(recipients.toArray())));
		
		return recipients;
	}

	List<String> getRecipientsForTeam(String ownerTeam) {
		Collection<PositionAwareComponent> candidateComponents = null;
		
		if (returnAll || (ownerTeam == null)) {
			candidateComponents = networkRegistry.getIpEnabledComponents();			
		} else {
			candidateComponents = new HashSet<>();
			
			//Find all areas of my team
			List<Area> areas = networkRegistry.getTeamSites(ownerTeam);				
			
			// handle teams deployed outside specifically
			if (areas.isEmpty()) {
				candidateComponents.addAll(networkRegistry.getComponentsOutside());
			} else {
				// get all components in those areas
				for (Area a: areas) {
					candidateComponents.addAll(networkRegistry.getComponentsInArea(a));
				}
			}
		}
		
		// returning an array list instead of something else is important since
		// we later rely on direct access by index
		List<String> recipients = new ArrayList<>();
		for (PositionAwareComponent c: candidateComponents) {
			if (c.hasIP)
				recipients.add(c.id);
		}
		return recipients;
	}
	
}