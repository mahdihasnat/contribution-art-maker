function getLevel(contribution, maxContribution) {
    const segmentSize = Math.floor(maxContribution / 4)
    const segments = [segmentSize, segmentSize, segmentSize, segmentSize];
    var reminder = maxContribution % 4;
    if (reminder > 0) {
        segments[3]++;
        reminder--;
    }
    if(reminder > 1) {
        segments[2] ++;
        reminder--;
    }
    if(reminder > 0) {
        segments[1] ++;
        reminder--;
    }
    console.assert(reminder === 0);
    for(let i = 0; i < segments.length; i++) {
        if(contribution <= segments[i]) {
            return i + 1;
        }
        contribution -= segments[i];
    }
    console.assert(false);
    return -1;
}
const table = document.getElementsByClassName('js-calendar-graph-table')[0]
const cells = table.querySelectorAll('[data-date],[data-level]')
const levelAndContribution = []
cells.forEach(cell => {
    const date = cell.getAttribute('data-date');
    const level = parseInt(cell.getAttribute('data-level'));
    const toolTipId = cell.getAttribute('aria-labelledby');
    const toolTip = document.getElementById(toolTipId);
    const toolTipText = toolTip.textContent;
    if(level > 0) {
        const contribution = parseInt(toolTipText.match(/(\d+) contribution/)[1]);
        levelAndContribution.push({level, contribution, date});
    }
});
const maxContribution = Math.max(...levelAndContribution.map(item => item.contribution));
console.log('Max contribution:', maxContribution);
levelAndContribution.forEach(({level, contribution, date}) => {
    let expectedLevel = getLevel(contribution, maxContribution);
    console.assert(level === expectedLevel, `Expected level ${expectedLevel}, got ${level} for contribution ${contribution} on date ${date}`);
});
console.log('All assertions passed');