let cy = null;


async function getJSON(url) {
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(
            `Request failed: ${response.status}`
        );
    }

    return response.json();
}


async function loadDashboard() {

    try {

        const [
            entities,
            relationships,
            analytics,
            graph
        ] = await Promise.all([
            getJSON("/api/entities"),
            getJSON("/api/relationships"),
            getJSON("/api/analytics"),
            getJSON("/api/graph")
        ]);


        document.getElementById(
            "entityCount"
        ).textContent = entities.length;


        document.getElementById(
            "relationshipCount"
        ).textContent = relationships.length;


        document.getElementById(
            "communityCount"
        ).textContent = analytics.communities;


        document.getElementById(
            "density"
        ).textContent = analytics.density;


        renderGraph(graph);

        renderEntities(
            analytics.top_entities
        );

    } catch (error) {

        console.error(error);

        alert(
            "Could not load dashboard data."
        );
    }
}


function renderGraph(graphData) {

    if (cy) {
        cy.destroy();
    }


    cy = cytoscape({

        container:
            document.getElementById("cy"),

        elements: [
            ...graphData.nodes,
            ...graphData.edges
        ],

        style: [

            {
                selector: "node",

                style: {

                    "background-color":
                        "#3b82f6",

                    "label":
                        "data(label)",

                    "color":
                        "#dbeafe",

                    "font-size":
                        "11px",

                    "text-valign":
                        "bottom",

                    "text-margin-y":
                        "7px",

                    "width":
                        "35px",

                    "height":
                        "35px",

                    "border-width":
                        2,

                    "border-color":
                        "#60a5fa"
                }
            },


            {
                selector:
                    'node[type="Organization"]',

                style: {
                    "background-color":
                        "#8b5cf6",

                    "shape":
                        "rectangle"
                }
            },


            {
                selector:
                    'node[type="Location"]',

                style: {
                    "background-color":
                        "#14b8a6",

                    "shape":
                        "diamond"
                }
            },


            {
                selector: "edge",

                style: {

                    "width":
                        "mapData(weight, 1, 5, 1, 5)",

                    "line-color":
                        "#35516f",

                    "target-arrow-color":
                        "#35516f",

                    "target-arrow-shape":
                        "triangle",

                    "curve-style":
                        "bezier",

                    "label":
                        "data(relationship)",

                    "font-size":
                        "7px",

                    "color":
                        "#6f89a6",

                    "text-rotation":
                        "autorotate"
                }
            }

        ],

        layout: {

            name:
                "cose",

            animate:
                true,

            padding:
                40,

            nodeRepulsion:
                7000,

            idealEdgeLength:
                120
        }

    });


    cy.on(
        "tap",
        "node",
        function(event) {

            const node =
                event.target;

            const data =
                node.data();

            console.log(
                "Selected entity:",
                data
            );
        }
    );
}


function renderEntities(entities) {

    const container =
        document.getElementById(
            "entitiesList"
        );


    if (!entities.length) {

        container.innerHTML =
            "<p>No entities found.</p>";

        return;
    }


    container.innerHTML =
        entities.map(entity => {

            return `
                <div
                    class="entity-item"
                    data-id="${entity.id}"
                >

                    <div class="entity-name">
                        ${entity.name}
                    </div>

                    <div class="entity-score">
                        Analytical score:
                        ${entity.score}
                    </div>

                </div>
            `;

        }).join("");


    document
        .querySelectorAll(".entity-item")
        .forEach(item => {

            item.addEventListener(
                "click",
                () => {

                    const id =
                        item.dataset.id;

                    if (cy) {

                        const node =
                            cy.getElementById(id);

                        if (node.length) {

                            cy.animate({
                                center: {
                                    eles: node
                                },
                                zoom: 2
                            });

                            node
                                .select();
                        }
                    }
                }
            );
        });
}


document
    .getElementById("resetGraph")
    .addEventListener(
        "click",
        () => {

            if (!cy) return;

            cy.elements()
                .unselect();

            cy.layout({
                name: "cose",
                animate: true,
                padding: 40
            }).run();

            cy.fit();
        }
    );


document
    .getElementById("analyzeButton")
    .addEventListener(
        "click",
        async () => {

            const text =
                document
                    .getElementById(
                        "analysisText"
                    )
                    .value.trim();


            if (!text) {

                alert(
                    "Enter some text first."
                );

                return;
            }


            const response =
                await fetch(
                    "/api/analyze-text",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            text: text
                        })
                    }
                );


            const result =
                await response.json();


            const output =
                document.getElementById(
                    "analysisResult"
                );


            if (result.error) {

                output.textContent =
                    result.error;

                return;
            }


            if (
                !result.entities ||
                result.entities.length === 0
            ) {

                output.textContent =
                    "No entities detected.";

                return;
            }


            output.innerHTML =
                "<strong>Detected entities:</strong><br><br>" +

                result.entities
                    .map(entity => {

                        return `
                            <span
                                class="entity-tag"
                            >
                                ${entity.text}
                                (${entity.label})
                            </span>
                        `;

                    })
                    .join("");
        }
    );


loadDashboard();
