-- Lua: tabeller, funksjoner, metatabeller og løkker
local G <const> = 6.674e-11
local Legeme = {}
Legeme.__index = Legeme

--[[ Blokkommentar
     over flere linjer ]]
function Legeme.ny(navn, masse)
  local self = setmetatable({}, Legeme)
  self.navn = navn or "ukjent"
  self.masse = masse or 1.0
  return self
end

function Legeme:kraft(annen, r)
  if r == 0 then error("avstand null: " .. self.navn) end
  return G * self.masse * annen.masse / r ^ 2
end

local planeter = { Legeme.ny("Jorda", 5.972e24), Legeme.ny("Mars", 6.4e23) }
for i, p in ipairs(planeter) do
  print(string.format("%d %s %.2e\n", i, p.navn, p.masse))
end
for k = 1, 10, 2 do if k % 3 == 0 then goto videre end ::videre:: end
while true do break end
repeat local x = #planeter until x > 0 and not nil
local tekst = [[
Lang streng
over linjer]]
local ok, feil = pcall(function(...) return select("#", ...) end, 1, 2)
return Legeme
