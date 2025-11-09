```journal-nav

```

<%*
const birthDate = new Date("1973-11-03");
const today = new Date(tp.date.now("YYYY-MM-DD"));
// Days
const lifeDay = Math.floor((today - birthDate) / (1000 * 60 * 60 * 24));
// Weeks
const lifeWeek = Math.floor(lifeDay / 7);
const lifeWeekPct = ((lifeWeek / 4000) * 100).toFixed(1); // 1 decimal place
// Months
let lifeMonth = (today.getFullYear() - birthDate.getFullYear()) * 12 + (today.getMonth() - birthDate.getMonth());
// Years
let lifeYear = today.getFullYear() - birthDate.getFullYear();
if (today.getMonth() < birthDate.getMonth() || (today.getMonth() === birthDate.getMonth() && today.getDate() < birthDate.getDate())) {
lifeYear--;
}
tR += `**Life Day:** ${lifeDay}\n**Life Week:** ${lifeWeek} (${lifeWeekPct}%)\n**Life Month:** ${lifeMonth}\n**Life Year:** ${lifeYear}`;
%>

---

- 
