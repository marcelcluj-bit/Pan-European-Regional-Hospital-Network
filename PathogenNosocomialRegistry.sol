// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title PathogenNosocomialRegistry
 * @dev Synchronizes AI nosocomial infection alerts across all 81 hospitals in the EU network
 */
contract PathogenNosocomialRegistry {
    struct PathogenAlert {
        uint256 hospitalNodeId;
        string pathogenName;
        string amrGeneProfile;
        bool containmentTriggered;
        uint256 timestamp;
    }

    mapping(uint256 => PathogenAlert[]) public hospitalAlerts;

    event AlertBroadcasted(uint256 indexed nodeId, string pathogen, string genes);

    function registerAIPathogenDetection(
        uint256 _nodeId,
        string memory _pathogen,
        string memory _genes,
        bool _autoContainment
    ) external {
        hospitalAlerts[_nodeId].push(PathogenAlert({
            hospitalNodeId: _nodeId,
            pathogenName: _pathogen,
            amrGeneProfile: _genes,
            containmentTriggered: _autoContainment,
            timestamp: block.timestamp
        }));

        emit AlertBroadcasted(_nodeId, _pathogen, _genes);
    }
}
