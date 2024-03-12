import EmailRange from "../Components/EmailRange";
import SeedRange from "../Components/SeedRange";

const Home = () => {
    const startDownload = () => {
        makeRequest('/download', null);        
    }

    const periodRequesting = async(endpoint, data) => {
        const splitValue = 10;
        // it needs to be delayed to ensure that backend does not manage to somehow process
        // the harder task faster even though improbable
        const delayInMs = 10000; // 10 seconds
        const stepSize = Math.ceil(data.value / splitValue);
    
        const increments = Array.from({ length: splitValue }, (_, i) => (i + 1) * stepSize);

        for (let i = 0; i < increments.length; i++) {
            makeRequest(endpoint, { value: increments[i], seed: data.seed, iteration: i + 1 });
            // Wait for 5 minutes or when the request is done - avoid spamming the backend with unnecessary requests
            await new Promise(resolve => setTimeout(resolve, delayInMs));
          }
    };

    const makeRequest = (endpoint, data) => {
        fetch(`http://localhost:5000${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Something went wrong');
            }
        }).then(data => {
            if(endpoint === '/visualize'){

                const visCount = data.visualization_count;
                if(!visCount) {
                    return;
                }
                const div = document.createElement('div');
                div.className = "bk-root";
                div.id = "plot" + visCount;
                div.style.display = 'flex';
                div.style.alignItems = 'center';
                div.style.justifyContent = 'center';

                const parsedPlot = JSON.parse(data.plot);
                //console.log(data.plot)
                window.Bokeh.embed.embed_item(parsedPlot, div.id);
                document.getElementById("root").appendChild(div);

                // prettify a bit
                const br = document.createElement('br');
                document.getElementById("root").appendChild(br);

            }
        }
        ).catch(error => {
            console.log(error);
        });
    }

    const cleanIframes = () => {
        const iframes = document.getElementsByTagName('iframe');
        const removeIframe = (iframe) => {
            return new Promise((resolve) => {
                iframe.onload = () => {
                    iframe.parentNode.removeChild(iframe);
                    resolve();
                };
            });
        };
        const removalPromises = Array.from(iframes).map(removeIframe);
        return Promise.all(removalPromises);
    };

    const embedSentences = () => {
        const count = document.getElementsByClassName('emailRangeInput')[0].value;
        const seed = document.getElementById('seedInput').value;
        cleanIframes();
        makeRequest('/embeddings', {value: count, seed: seed});
    }

    const launchVisualization = () => {
        const count = document.getElementsByClassName('emailRangeInput')[1].value;
        const seed = document.getElementById('seedInput').value;
        cleanIframes();
        periodRequesting('/visualize', {value: count, seed: seed});
    }

    return (
        <div>
            <h1>Text Based Retrieval on Enron Email Dataset</h1>
            <div>

                <label className="emailCount">Seed:<SeedRange/> </label>
                <br/>
                <button onClick={startDownload}>Download Dataset</button>

                <label>
                Select the number of emails to embed:<EmailRange />
                </label>
                <br/>
                <button className="embed" onClick={embedSentences}>Embed Emails</button>

                <label className="emailCount">
                Select the number of emails to cluster:
                <EmailRange/>
                </label>
                <br/>
                <button onClick={launchVisualization}>Run Experiment</button>
            </div>
            <div id="plot"></div>
        </div>

    );
}

export default Home;