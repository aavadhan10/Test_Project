"use client";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function Dashboard() {
    const [token, setToken] = useState<string | null>(null);

    useEffect(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const authCode = urlParams.get("code");

        if (authCode) {
            fetch(`http://localhost:8000/callback?code=${authCode}`)
                .then(res => res.json())
                .then(data => {
                    setToken(data.access_token);
                    localStorage.setItem("clio_token", data.access_token);
                });
        } else {
            const storedToken = localStorage.getItem("clio_token");
            if (storedToken) setToken(storedToken);
        }
    }, []);

    return (
        <div className="container mx-auto p-6">
            <Card>
                <CardHeader>
                    <CardTitle>Clio Dashboard</CardTitle>
                </CardHeader>
                <CardContent>
                    {!token ? (
                        <Button asChild>
                            <a href="http://localhost:8000/login">Login with Clio</a>
                        </Button>
                    ) : (
                        <Button onClick={() => alert("Fetching Data...")}>Fetch Clio Data</Button>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}
